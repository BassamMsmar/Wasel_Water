from django.urls import path
from .views import CartList, cart_add, cart_update

app_name = 'cart'
urlpatterns = [
    path('', CartList.as_view(), name='cart_detail'),
    path('add/', cart_add, name='cart_add'),
    path('update/', cart_update, name='cart_update'),
]
