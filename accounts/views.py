from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add summary data to dashboard if needed, e.g., last 3 orders
        user = self.request.user
        context['recent_orders'] = user.orders.all()[:5]
        return context

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/settings.html'

class AddressListView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/address_list.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile_detail.html'
    
    def post(self, request, *args, **kwargs):
        # Placeholder for profile update logic
        return render(request, self.template_name, {'success': True})

class PaymentMethodsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/payment_methods.html'
