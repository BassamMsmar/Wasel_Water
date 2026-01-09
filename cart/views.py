from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart

# Create your views here.
class CartList(TemplateView):
    template_name = 'cart/cart_detail.html'

from django.template.loader import render_to_string

@require_POST
def cart_add(request):
    try:
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        if not product_id:
            return JsonResponse({'error': 'No product ID provided'}, status=400)
            
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)

        # Render sidebar HTML
        cart_html = render_to_string('cart/partials/sidebar_cart.html', {'cart': cart}, request=request)

        return JsonResponse({
            'qty': len(cart), 
            'message': 'تم إضافة المنتج للسلة بنجاح',
            'cart_html': cart_html
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
def cart_update(request):
    try:
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=quantity, override_quantity=True)

        cart_html = render_to_string('cart/partials/sidebar_cart.html', {'cart': cart}, request=request)
        
        return JsonResponse({
            'qty': len(cart), 
            'message': 'تم تحديث السلة',
            'cart_html': cart_html,
            'total_price': cart.get_total_price(),
            'item_total': cart.cart[str(product_id)]['price'] * quantity # approximate, better to get from cart item
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
