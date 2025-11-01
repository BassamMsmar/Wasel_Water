from django.shortcuts import render
from products.models import Product, Categories
from django.db.models import Count

# Create your views here.
def home(request):
    """
    Display the home page with featured products, categories, and ads.
    """


    # Get featured products (you can adjust the filtering logic as needed)
    # featured_products = Product.objects.filter(active=True)[:8]  # Get 8 active products
    
    # # Get main categories (you might want to adjust this based on your category structure)
    # main_categories = Categories.objects.filter(parent__isnull=True)[:6]  # Get top 6 main categories
    
    # Get latest products
    # latest_products = Product.objects.filter(active=True).order_by('-created_at')[:6]
    latest_products = Product.objects.filter(active=True)[:6]
    
    # Get best selling products (you'll need to implement this logic based on your sales data)
    # best_selling = Product.objects.filter(active=True).annotate(
    #     order_count=Count('order_items')
    # ).order_by('-order_count')[:6]
    
    # You can add more queries for ads, special offers, etc.
    
    context = {
        # 'featured_products': featured_products,
        # 'main_categories': main_categories,
        'latest_products': latest_products,
        # 'best_selling': best_selling,
        # Add more context variables as needed
    }
    
    return render(request, 'home.html', context)