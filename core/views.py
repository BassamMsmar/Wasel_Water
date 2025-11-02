from django.shortcuts import render
from products.models import Product, Offer, Brand, Category
from django.db.models import Count


from .models import Banner

# Create your views here.
def home(request):
    """
    Display the home page with featured products, categories, and ads.
    """


    # Get featured products (you can adjust the filtering logic as needed)
    # featured_products = Product.objects.filter(active=True)[:8]  # Get 8 active products
    
    # # Get main categories (you might want to adjust this based on your category structure)
    # main_categories = Category.objects.filter(parent__isnull=True)[:6]  # Get top 6 main categories
    
    # Get latest products
    # latest_products = Product.objects.filter(active=True).order_by('-created_at')[:6]

    #products 
    offers = Offer.objects.all()
    latest_products = Product.objects.filter(active=True)[:10]
    bundle_products = Product.objects.filter(product_type='bundle')[:6]
    banners = Banner.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.all()
    # Get best selling products (you'll need to implement this logic based on your sales data)
    # best_selling = Product.objects.filter(active=True).annotate(
    #     order_count=Count('order_items')
    # ).order_by('-order_count')[:6]
    
    # You can add more queries for ads, special offers, etc.
    

    #banners
    banner_offer = Banner.objects.filter(type='offer')
    banner_bundle = Banner.objects.filter(type='bundle')

    context = {
        # 'featured_products': featured_products,
        # 'main_categories': main_categories,
        'latest_products': latest_products,
        'offers': offers,
        'bundle_products': bundle_products,
        'banners': banners,
        'brands': brands,
        'categories': categories,
        # 'best_selling': best_selling,
        # Add more context variables as needed
    }
    
    return render(request, 'home.html', context)