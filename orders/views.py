from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Order

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # Return all orders effectively, or just completed ones if strict separation is needed
        # User requested "Orders (Paid/Old/New)" vs "Pending (Waiting Payment)"
        # So here we exclude pending/cancelled maybe?
        # Let's show all non-pending for "Orders" to be safe, or just "Paid/Shipped/Delivered"
        return Order.objects.filter(user=self.request.user).exclude(status='pending').exclude(status='cancelled')

class PendingOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html' # Reuse template or create separate one
    context_object_name = 'orders'
    extra_context = {'is_pending': True}

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='pending')

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
         return Order.objects.filter(user=self.request.user)

class PaymentSelectionView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/payment_selection.html'
    context_object_name = 'order'

    def get_queryset(self):
         return Order.objects.filter(user=self.request.user, status='pending')

class CompletePaymentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user, status='pending')
        payment_method = request.POST.get('payment_method')
        
        if payment_method == 'cod':
            # Here we might update status to 'processing' or keep 'pending' but mark as confirmed method
            # For now, let's just show success and go to detail
            messages.success(request, 'تم اختيار طريقة الدفع بنجاح. سنقوم بتجهيز طلبك.')
            return redirect('orders:detail', pk=order.pk)
        
        messages.error(request, 'طريقة الدفع غير صحيحة')
        return redirect('orders:payment_selection', pk=order.pk)
