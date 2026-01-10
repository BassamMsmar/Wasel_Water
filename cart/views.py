from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product, Bundle
from .cart import Cart

# Create your views here.
class CartList(TemplateView):
    template_name = 'cart/cart_detail.html'

class CartCheckout(TemplateView):
    template_name = 'cart/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context

from django.template.loader import render_to_string

@require_POST
def cart_add(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    item_type = request.POST.get('item_type', 'product') # Default to product
    
    if not product_id:
        return JsonResponse({'error': 'No ID provided'}, status=400)
        
    try:
        if item_type == 'bundle':
            product = get_object_or_404(Bundle, id=product_id)
        else:
            product = get_object_or_404(Product, id=product_id)
            
        cart.add(product=product, item_type=item_type)
        
        # Generate the updated cart HTML
        cart_html = render_to_string('cart/partials/sidebar_cart.html', {'cart': cart}, request=request)
        
        return JsonResponse({
            'success': True, 
            'cart_count': len(cart),
            'cart_html': cart_html,
            'message': 'تمت الإضافة للسلة بنجاح'
        })
    except Exception as e:
         return JsonResponse({'error': str(e)}, status=500)

@require_POST
def cart_update(request):
    try:
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        item_type = request.POST.get('item_type', 'product')
        
        if item_type == 'bundle':
            product = get_object_or_404(Bundle, id=product_id)
        else:
            product = get_object_or_404(Product, id=product_id)
            
        cart.add(product=product, quantity=quantity, override_quantity=True, item_type=item_type)

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

@require_POST
def cart_remove(request):
    try:
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        item_type = request.POST.get('item_type', 'product')
        
        # We don't need to fetch the object to remove it, just ID and type
        cart.remove(product_id, item_type=item_type)
        
        cart_html = render_to_string('cart/partials/sidebar_cart.html', {'cart': cart}, request=request)
        
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_html': cart_html,
            'cart_total': cart.get_total_price(),
            'message': 'Item removed'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
