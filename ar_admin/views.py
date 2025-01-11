from django.shortcuts import render
from ar_store.models import ProductRegistration
from ar_payment.models import OrderSummary
from django.shortcuts import get_object_or_404, render,redirect
from ar_store.models import ProductRegistration,Category
from .forms import ProductRegistrationForm
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.utils import timezone
from django.http import Http404
from django.core.paginator import Paginator
from ar_store.models import Contact




def admin_home(request):
    if request.user.is_authenticated:
        count = ProductRegistration.objects.count()
        order_count = OrderSummary.objects.count()
        completed_order_count = OrderSummary.objects.filter(is_shipped=True).count()
        return render(request, 'admin_home.html',{'count':count,'order_count':order_count,'completed_order_count':completed_order_count})
    else:
        # Raise a 404 error if the user is not authenticated
        raise Http404("Page not found")
    



def all_products(request):
    if request.user.is_authenticated:
        # Get the total count of products
        count = ProductRegistration.objects.count()
        
        # Get the search query from the request, default to an empty string if not present
        q = request.GET.get('q', '')  

        # Initialize query_count as None or 0 initially
        query_count = 0  # Default to 0 if there is no query

        # Only perform the query and count if q is not empty
        if q:
            products = ProductRegistration.objects.filter(
                Q(category__name__icontains=q) |
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(price__icontains=q) |
                Q(discount_price__icontains=q)
            ).order_by('-id')

            # Get the count of the filtered products
            query_count = products.count()
        else:
            # If no query string, return all products
            products = ProductRegistration.objects.all().order_by('-id')

        # Get all categories for the dropdown or filter options
        categorys = Category.objects.all()
        
        # Pagination: Show 12 items per page on large screens and 8 items per page on small screens
        items_per_page = 12  # Default for large screens

        # Adjust the number of items per page based on screen size (use query param or user-agent)
        if 'small' in request.GET:  # Check if small screen pagination is requested
            items_per_page = 8

        paginator = Paginator(products, items_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Pass paginated products (page_obj) and other context variables to the template
        context = {
            'products': page_obj,
            'categorys': categorys,
            'count': count,
            'query_count': query_count,
            'q': q,  # Pass the search term to the template
        }

        return render(request, "all-products.html", context)
    else:
        # Raise a 404 error if the user is not authenticated
        raise Http404("Page not found")




def add_product(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ProductRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                # Generate the URL for the "All Products" page
                all_products_url = reverse('all-products')  # Use the correct URL name
                # Create a success message with an anchor tag
                messages.success(request, mark_safe(f'Product added successfully! <a href="{all_products_url}">View all products</a>'))
                # Render the same page with the success message
                return render(request, 'add-product.html', {'form': form})
        else:
            form = ProductRegistrationForm()

        return render(request, 'add-product.html', {'form': form})
    else:
        # Raise a 404 error if the user is not authenticated
        raise Http404("Page not found")

def delete_product(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(ProductRegistration, id=pk)
        product.delete()
        messages.success(request, f'{product.name} deleted successfully!')
        return redirect('all-products')  # Redirect to the all products page
    else:
        # Raise a 404 error if the user is not authenticated
        raise Http404("Page not found")
    

def all_orders(request):
    if request.user.is_authenticated:
        q = request.GET.get('q', '')  # Get the search query

        filters = Q()

        if q:
            try:
                parsed_date = parse_datetime(q)
                if parsed_date:
                    filters &= Q(orderd_date=parsed_date.date())
                else:
                    filters |= Q(order_id__icontains=q)
                    filters |= Q(orderd_date__icontains=q)
                    filters |= Q(razorpay_id__icontains=q)
            except ValueError:
                pass

        # Get the current date in the local time zone (Asia/Kolkata)
        today = timezone.localtime(timezone.now()).date()

        # Get orders based on filters
        orders = OrderSummary.objects.filter(filters).order_by('-id')

        return render(request, 'all-orders.html', {'orders': orders, 'today': today})
    else:
        raise Http404("Page not found")


    

def order_details(request,pk):
    if request.user.is_authenticated:
        order = get_object_or_404(OrderSummary, order_id=pk)
        return render(request, 'order_details.html', {'order': order,'order_products': order.order_products})
    else:
        # Raise a 404 error if the user is not authenticated
        raise Http404("Page not found")
    



def details(request,pk):
    if request.user.is_authenticated:
        details = get_object_or_404(ProductRegistration, id=pk)
        if request.method == 'POST':
            form = ProductRegistrationForm(request.POST, request.FILES, instance=details)
            if form.is_valid():
                form.save()
                messages.success(request, f'{details.name} details updated successfully!')
                return redirect('all-products')  # Redirect to the product detail page after update
        else:
            form = ProductRegistrationForm(instance=details)

        categories = Category.objects.all()  # Assuming you have a Category model
        return render(request, 'admin-product-details.html', {'details': details, 'form': form, 'categories': categories})
    else:
        # Raise a 404 error if the user is not authenticated
        raise Http404("Page not found")
   


def product_shipping(request):
    if request.user.is_authenticated:
            # Get the search query from the GET request, default to empty string if not provided
        q = request.GET.get('q', '') 

        # Initialize the filters object
        filters = Q()

        if q:
            # Handle search logic for date and order_id
            try:
                # Attempt to parse q as a datetime with 12-hour format
                try:
                    parsed_date = datetime.strptime(q, "%Y-%m-%d %I:%M %p")  # 12-hour format
                    filters &= Q(orderd_date__date=parsed_date.date())  # Filter by date only
                except ValueError:
                    # If not in 12-hour format, try 24-hour format
                    parsed_date = parse_datetime(q)
                    if parsed_date:
                        filters &= Q(orderd_date__date=parsed_date.date())  # Filter by date if valid
                    else:
                        raise ValueError("Invalid date format")

            except ValueError:
                # If q is not a date, continue filtering by order_id and orderd_date (with icontains for string search)
                filters |= Q(order_id__icontains=q)  # Filter orders by order_id (substring match)
                filters |= Q(orderd_date__icontains=q)  # If it's a string like "2024-12", filter by date (contains match)
                filters |= Q(shipped_date__icontains=q)  # If it's a string match for shipped date (also supports date search)


        # Get the current date in the local time zone (Asia/Kolkata)
        today = timezone.localtime(timezone.now()).date()

        # Get the filtered orders based on the filters (if any)
        orders = OrderSummary.objects.filter(filters).order_by('-id')

        # Split the orders into shipped and not shipped
        shipped_orders = orders.filter(is_shipped=True)
        not_shipped_orders = orders.filter(is_shipped=False)

        return render(request, 'product-shipping.html', {
            'shipped_orders': shipped_orders,
            'not_shipped_orders': not_shipped_orders,
            'today' : today,
        })
    else:
        # Raise a 404 error if the user is not authenticated
        raise Http404("Page not found")
    



def completed_orders(request):
    if request.user.is_authenticated:
            # Get the search query from the GET request, default to empty string if not provided
        q = request.GET.get('q', '') 

        # Initialize the filters object
        filters = Q()

        if q:
            # Handle search logic for date and order_id
            try:
                # Attempt to parse q as a datetime with 12-hour format
                try:
                    parsed_date = datetime.strptime(q, "%Y-%m-%d %I:%M %p")  # 12-hour format
                    filters &= Q(orderd_date__date=parsed_date.date())  # Filter by date only
                except ValueError:
                    # If not in 12-hour format, try 24-hour format
                    parsed_date = parse_datetime(q)
                    if parsed_date:
                        filters &= Q(orderd_date__date=parsed_date.date())  # Filter by date if valid
                    else:
                        raise ValueError("Invalid date format")

            except ValueError:
                # If q is not a date, continue filtering by order_id and orderd_date (with icontains for string search)
                filters |= Q(order_id__icontains=q)  # Filter orders by order_id (substring match)
                filters |= Q(orderd_date__icontains=q)  # If it's a string like "2024-12", filter by date (contains match)
                filters |= Q(shipped_date__icontains=q)  # If it's a string match for shipped date (also supports date search)

        # Get the filtered orders based on the filters (if any)
        orders = OrderSummary.objects.filter(filters).order_by('-id')

        # Split the orders into shipped and not shipped
        shipped_orders = orders.filter(is_shipped=True)
        return render(request, 'completed-orders.html', {
            'shipped_orders': shipped_orders
        })
    else:
        # Raise a 404 error if the user is not authenticated
        raise Http404("Page not found")
    



def mark_as_not_shipped(request, order_id):
    if request.user.is_authenticated:
        # Fetch the order by ID
        order = get_object_or_404(OrderSummary, id=order_id)
        
        # Update the `is_shipped` field
        order.is_shipped = False
        order.save()
        
        # Add a success message (optional)
        messages.success(request, f"Order {order.order_id} has been marked as not shipped.")
    
        # Redirect to a page (e.g., the orders list or the same page)
        return redirect('product-shipping')  # Replace 'orders_list' with your desired view name
    else:
        # Raise a 404 error if the user is not authenticated
        raise Http404("Page not found")
    

def mark_as_shipped(request, order_id):
    if request.user.is_authenticated:
        # Fetch the order by ID
        order = get_object_or_404(OrderSummary, id=order_id)
        
        # Check if the order is already shipped
        if order.is_shipped:
            messages.info(request, f"Order {order.order_id} has already been marked as shipped.")
        else:
            # Update the `is_shipped` field
            order.is_shipped = True
            order.shipped_date = timezone.now()  # Optionally, update the shipped date to now
            order.save()
            
            # Add a success message
            messages.success(request, f"Order {order.order_id} has been marked as shipped.")
        
        # Redirect to a page (e.g., the orders list or the same page)
        return redirect('product-shipping')  # Replace 'orders_list' with your desired view name
    else:
        # Raise a 404 error if the user is not authenticated
        raise Http404("Page not found")
    



def all_contacts(request):
    if request.user.is_authenticated:
        q = request.GET.get('q') if request.GET.get('q') != None else ''   

        contacts = Contact.objects.filter(Q(email__icontains=q) | Q(phone__icontains=q) | Q(id__icontains=q)).order_by('-id')
        for contact in contacts:
            contact.date_added = timezone.localtime(contact.date_added)
        return render(request, 'all-contacts.html', {'contacts': contacts,})
    else:
        # Raise a 404 error if the user is not authenticated
        raise Http404("Page not found")