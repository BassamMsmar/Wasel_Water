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
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)

    # Render sidebar HTML
    cart_html = render_to_string('cart/partials/sidebar_cart.html', {'cart': cart}, request=request)

    return JsonResponse({
        'qty': len(cart), 
        'message': 'تم إضافة المنتج للسلة بنجاح',
        'cart_html': cart_html
    })
