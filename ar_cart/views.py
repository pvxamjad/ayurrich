from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from ar_payment.models import OrderProducts
from ar_store.models import ProductRegistration
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.



def cart(request):
    # get the cart 
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()

    product_totals = {}

    try:
        product_totals = {
            str(product.id): product.discount_price * int(
                quantities.get(str(product.id), {}).get("quantity", 0)
                if isinstance(quantities.get(str(product.id), {}), dict)
                else quantities.get(str(product.id), 0)
            )
            for product in cart_products
        }
    except (TypeError, ValueError) as e:
        print("Error calculating product totals:", e)

        
    # Calculate subtotal
    subtotal = sum(product_totals.values())
    
    delivery_charge = 40

    subtotal_delivery = subtotal + int(delivery_charge)    

    return render(request, 'cart.html',{'cart_products':cart_products,'quantities':quantities,'product_totals':product_totals,'subtotal':subtotal,'subtotal_delivery':subtotal_delivery})

def add_cart(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(ProductRegistration, id=product_id)

        # Add to cart session
        cart.add(product=product, quantity=product_qty)

        # Add to OrderProducts model (this stores the data in the DB)
        session_id = request.session.session_key
        price = product.discount_price
        total_price = price * product_qty

        # Add or update the product in the OrderProducts model
        order_product, created = OrderProducts.objects.update_or_create(
            session_id=session_id,
            product=product,
            defaults={
                'quantity': product_qty,
                'price': price,
                'total_price': total_price,
            }
        )

        cart_quantity = cart.__len__()

        success_message = f"{product.name} has been added to your cart."
        response_data = {
            'message': success_message,
            'qty': cart_quantity,
        }

        return JsonResponse(response_data)
    
    return JsonResponse({'message': 'Error'}, status=400)    
    


def update_cart_qty(request):
    if request.POST.get('action') == 'update':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # Ensure quantity is between 1 and 20
        product_qty = min(20, max(1, product_qty))

        cart = Cart(request)
        product = get_object_or_404(ProductRegistration, id=product_id)

        # Update the cart session
        cart.update(product=product, quantity=product_qty)

        # Update the OrderProducts model
        session_id = request.session.session_key
        price = product.discount_price
        total_price = price * product_qty

        # Update the existing OrderProduct or create a new one
        order_product, created = OrderProducts.objects.update_or_create(
            session_id=session_id,
            product=product,
            defaults={
                'quantity': product_qty,
                'price': price,
                'total_price': total_price,
            }
        )

        cart_quantity = cart.__len__()
        success_message = f"The quantity of {product.name} has been updated to {product_qty}."

        return JsonResponse({
            'message': success_message,
            'qty': cart_quantity,
        })
def remove_cart_item(request):
    cart = Cart(request)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(ProductRegistration, id=product_id)

        # Remove from cart session
        cart.remove(product)

        # Remove from OrderProducts model
        session_id = request.session.session_key
        try:
            order_product = OrderProducts.objects.get(session_id=session_id, product=product)
            order_product.delete()
        except OrderProducts.DoesNotExist:
            pass  # If the product is not found in OrderProducts, just pass

        return JsonResponse({'success': True, 'message': 'Product removed from cart'})
    else:
        return redirect('cart')  # Redirect to the cart page if it's not a POST request