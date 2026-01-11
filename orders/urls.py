from django.urls import path
from .views import OrderListView, PendingOrderListView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='list'),
    path('pending/', PendingOrderListView.as_view(), name='pending_list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='detail'),
]
