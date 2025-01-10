from django.shortcuts import render, redirect
from .models import OrderProducts, ShippingAddress, OrderSummary
from ar_cart.cart import Cart
from ar_store.models import ProductRegistration
from .forms import ShippingForm
import razorpay
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404
import logging
import pytz
from .utils import send_order_email  # Import the email function
from django.conf import settings
from .razorpay import RazorpayClient  # Import your Razorpay wrapper class

logger = logging.getLogger(__name__)

@csrf_exempt
def create_razorpay_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = data.get("amount", 0)  # Amount in paisa (1 INR = 100 paisa)
            receipt = data.get("receipt", "order_rcptid_11")

            razorpay_client = RazorpayClient()
            order = razorpay_client.create_order(amount=amount, currency="INR", payment_capture=1)
            return JsonResponse({"success": True, **order})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method"})

@csrf_exempt
def verify_razorpay_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            razorpay_client = RazorpayClient()
            razorpay_client.verify_signature(data)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method"})

def billing(request):
    # Ensure session exists
    if not request.session.session_key:
        request.session.create()

    session_id = request.session.session_key
    # Get cart data from session
    cart_data = request.session.get('session_key', {})
    
    if not cart_data:
        return redirect('cart')  # Redirect if cart is empty

    # Calculate subtotal from cart data
    product_totals = {}
    subtotal = 0
    for product_id, quantity in cart_data.items():
        try:
            product = ProductRegistration.objects.get(id=product_id)
            price = product.discount_price
            total_price = price * quantity
            product_totals[product_id] = total_price
            subtotal += total_price
        except ProductRegistration.DoesNotExist:
            print(f"Product with ID {product_id} does not exist.")

    # Add delivery charge condition
    delivery_charge = 0 if subtotal > 500 else 40
    total = subtotal + delivery_charge

    # Handle item removal from cart (if applicable)
    if 'remove_from_cart' in request.GET:
        product_id_to_remove = request.GET.get('remove_from_cart')
        
        # Delete the product from OrderProducts for the current session
        deleted_count, _ = OrderProducts.objects.filter(session_id=session_id, product_id=product_id_to_remove).delete()
        if deleted_count > 0:
            print(f"Successfully deleted OrderProduct with product_id: {product_id_to_remove}")
        else:
            print(f"OrderProduct with product_id {product_id_to_remove} not found.")

        # Remove the item from the session cart as well
        if product_id_to_remove in cart_data:
            del cart_data[product_id_to_remove]  # Remove product from cart
            request.session['session_key'] = cart_data  # Update session data
            request.session.modified = True
            print(f"Removed product {product_id_to_remove} from session cart.")

        return redirect('billing')  # Redirect back to the billing page after removal

    # Update or create OrderProducts based on cart data
    for product_id, quantity in cart_data.items():
        try:
            product = ProductRegistration.objects.get(id=product_id)
            price = product.discount_price
            total_price = price * quantity

            # Update existing OrderProducts or create new ones
            order_product, created = OrderProducts.objects.update_or_create(
                session_id=session_id,
                product=product,
                defaults={
                    'quantity': quantity,
                    'price': price,
                    'total_price': total_price,
                },
            )
            if created:
                print(f"Created OrderProduct for Product {product.name}")
            else:
                print(f"Updated OrderProduct for Product {product.name}")

        except ProductRegistration.DoesNotExist:
            print(f"Product with ID {product_id} does not exist.")
        except Exception as e:
            print(f"Error processing product {product_id}: {e}")

    # Check for existing shipping address in session
    shipping_address_id = request.session.get('shipping_address_id')
    shipping_address = None
    if shipping_address_id:
        shipping_address = ShippingAddress.objects.filter(id=shipping_address_id).first()

    # Create or fetch shipping form instance
    form_data = request.session.get('shipping_address', {})
    form = ShippingForm(instance=shipping_address) if shipping_address else ShippingForm(initial=form_data)

    # Handle the form submission (POST request)
    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping_address)
        if form.is_valid():
            # Set 'country' to 'India' explicitly if it's not submitted
            updated_shipping_address = form.save(commit=False)
            if not updated_shipping_address.country:  # If the field is empty
                updated_shipping_address.country = "India"
            updated_shipping_address.save()
            # Save shipping address in the session
            request.session['shipping_address'] = {
                'full_name': updated_shipping_address.full_name,
                'email': updated_shipping_address.email,
                'address': updated_shipping_address.address,
                'city': updated_shipping_address.city,
                'state': updated_shipping_address.state,
                'pincode': updated_shipping_address.pincode,
                'country': updated_shipping_address.country,
            }
            request.session['shipping_address_id'] = updated_shipping_address.id
            request.session.modified = True

            # Redirect after form submission
            return redirect('billing')

    # Fetch saved cart details
    order_products = OrderProducts.objects.filter(session_id=session_id)

    # Pass the shipping address existence flag to the template
    is_address_saved_in_db = bool(shipping_address)

    return render(request, 'billing.html', {
        'form': form,
        'order_products': order_products,  # Pass saved cart details to the template
        'subtotal': subtotal,  # Pass subtotal to the template
        'delivery_charge': delivery_charge,  # Pass delivery charge to the template
        'total': total,  # Pass total to the template
        'is_address_saved_in_db': is_address_saved_in_db,  # Flag to indicate if address is saved
        'RAZORPAY_KEY_ID': settings.RAZORPAY_KEY_ID, #passing razorpay key
    })

@csrf_exempt
def save_order_summary(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.debug("Received data: %s", data)

            # Retrieve order_products as is (since it's already a structured list of dictionaries)
            order_products = data.get('order_products', [])

            current_time = timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))
            # Save the order summary
            order_id = f"ORDER_{int(current_time.strftime('%Y%m%d%H%M%S'))}"
            order_summary = OrderSummary.objects.create(
                order_id=order_id,
                shipping_info=data.get('shipping_info', {}),
                order_products=order_products,  # Save the structured list directly
                total_amount=data.get('total_amount', 0),
                
            )

            if order_summary:

                # Call the function to send email after order is created
                send_order_email(order_summary)

                
                # Clear the cart
                cart = Cart(request)
                cart.clear()

                 # Remove the products from OrderProducts model based on session ID
                session_id = request.session.session_key
                OrderProducts.objects.filter(session_id=session_id).delete()

                request.session['success_message'] = "Your order has been placed successfully!"

                return JsonResponse({'success': True, 'order_id': order_summary.order_id})

        except Exception as e:
            logger.error("Error saving order summary: %s", str(e))
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False}, status=400)

def payment_success(request):
    order_id = request.GET.get('order_id')
    order_summary = get_object_or_404(OrderSummary, order_id=order_id)  # Fetch the order summary

    success_message = request.session.pop('success_message', None)

    context = {
        'order_summary': order_summary,
        'shipping_info': order_summary.shipping_info,  # Assuming shipping_info is a JSONField or similar
        'success_message':success_message,
    }


    return render(request, 'payment_success.html', context)



