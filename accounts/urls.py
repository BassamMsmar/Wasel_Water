from django.urls import path
from .views import DashboardView, SettingsView, AddressListView, ProfileView, PaymentMethodsView

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile_detail'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('addresses/', AddressListView.as_view(), name='address_list'),
    path('payment-methods/', PaymentMethodsView.as_view(), name='payment_methods'),
]
