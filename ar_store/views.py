from django.shortcuts import render
from .models import ProductRegistration,Category
from django.db.models import Q
from django.http import JsonResponse
from .models import Contact,Review
import json
from django.core.paginator import Paginator
from datetime import datetime
from django.db.models import Avg, Count

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

def product_dtails(request,pk):

    product = ProductRegistration.objects.get(id=pk)
    reviews = Review.objects.filter(product_name__icontains=product.name)
    health_benefits = product.health_benefits

    fullstar = Review.objects.filter(product_name__icontains=product.name, rating=5)[:4]
    # Calculate average rating
    average_rating = reviews.aggregate(average=Avg('rating'))['average']
    average_rating = round(average_rating, 1) if average_rating else 0

        # Count ratings
    rating_counts = reviews.values('rating').annotate(count=Count('rating'))
    total_reviews = reviews.count()

    # Initialize counts for all 5 stars (default to 0 if no reviews exist)
    rating_distribution = {i: 0 for i in range(1, 6)}
    for entry in rating_counts:
        rating_distribution[entry['rating']] = entry['count']

    # Calculate percentages for each star rating
    rating_percentages = {
        rating: (count / total_reviews * 100) if total_reviews > 0 else 0
        for rating, count in rating_distribution.items()
    }
    sorted_rating_percentages = dict(sorted(rating_percentages.items(), reverse=True))


    # Paginate reviews (10 per page)
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if product.health_benefits:
        health_benefits = health_benefits.split(sep='•')
        

        
        health_benefits = filter(None, health_benefits)
        return render(request, "product_detail.html" , {'product':product,
                                                        'health_benefits':health_benefits,
                                                        'reviews': page_obj,
                                                        'fullstar':fullstar,
                                                        'average_rating': average_rating,
                                                        'stars_range': range(1, 6),
                                                        'rating_distribution': rating_distribution,
                                                        'sorted_rating_percentages': sorted_rating_percentages,
                                                        })
    else:
    
        return render(request, "product_detail.html" , {'product':product})
    
def shop(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''   
    sort_by = request.GET.get('sort_by')  # Get the sorting option from query parameters
    
    products = ProductRegistration.objects.filter(Q(category__name__icontains=q) |
                                                  Q(name__icontains=q) |
                                                  Q(description__icontains=q) |
                                                  Q(price__icontains=q) |
                                                  Q(discount_price__icontains=q)
                                                  ).order_by('-id')

    categorys = Category.objects.all()
       # Pagination: Show 12 items per page on large screens and 8 items per page on small screens
    items_per_page = 12  # Default for large screens


    # Apply sorting based on the `sort_by` value
    if sort_by == 'price_low_to_high':
        products = products.order_by('discount_price')  # Sort by price ascending
    elif sort_by == 'price_high_to_low':
        products = products.order_by('-discount_price')  # Sort by price descending


    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass paginated products (page_obj) to the template
    context = {
        'products': page_obj,
        'categorys': categorys,
        'current_sort': sort_by,
    }
    return render(request, "shop.html" , context)

def submit_review(request):
    if request.method == "POST":
        customer_name = request.POST.get('customer_name')
        product_name = request.POST.get('product_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

        # Save to the database
        review = Review.objects.create(
            customer_name=customer_name,
            product_name=product_name,
            email=email,
            phone=phone,
            rating=rating,
            review_text=review_text
        )
        review.save()

        # Redirect or send success response
        return JsonResponse({'message': 'Review submitted successfully!'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)