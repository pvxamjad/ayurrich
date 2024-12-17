from django.shortcuts import render
from .models import ProductRegistration,Category
from django.db.models import Q
from django.http import JsonResponse
from .models import Contact
import json
from django.core.paginator import Paginator
from datetime import datetime


def save_contact(request):
    if request.method == 'POST':
        try:
            # Parse JSON body
            data = json.loads(request.body)

            # Extract email and phone from the request
            email = data.get('email')
            phone = data.get('phone')

            if not email or not phone:
                return JsonResponse({'message': 'Email and phone are required.'}, status=400)

            # Save the contact information to the database
            Contact.objects.create(email=email, phone=phone)

            # Respond with success
            return JsonResponse({'message': 'Contact saved successfully!'})

        except json.JSONDecodeError:
            # Handle invalid JSON input
            return JsonResponse({'message': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            # Handle unexpected errors
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)





def home(request):

    products = ProductRegistration.objects.all()[:4]

    return render(request, "home.html" , {'products':products})



def product_dtails(request,name):

    product = ProductRegistration.objects.get(name=name)
    health_benefits = product.health_benefits

    if product.health_benefits:
        health_benefits = health_benefits.split(sep='•')
        

        
        health_benefits = filter(None, health_benefits)
        return render(request, "product_detail.html" , {'product':product,'health_benefits':health_benefits})
    else:
    
        return render(request, "product_detail.html" , {'product':product})
    



def shop(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''   

    products = ProductRegistration.objects.filter(Q(category__name__icontains=q) |
                                                  Q(name__icontains=q) |
                                                  Q(description__icontains=q) |
                                                  Q(price__icontains=q) |
                                                  Q(discount_price__icontains=q)
                                                  ).order_by('-id')

    categorys = Category.objects.all()
       # Pagination: Show 12 items per page on large screens and 8 items per page on small screens
    items_per_page = 12  # Default for large screens


    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass paginated products (page_obj) to the template
    context = {
        'products': page_obj,
        'categorys': categorys,
    }
    return render(request, "shop.html" , context)



