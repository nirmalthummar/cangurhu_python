from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib.auth import get_user_model

from apps.order.models import OrderMenuSubItem, Order, OrderMenuItem
from apps.courier.models import CourierOrder
from apps.cook.models import CookOrderDetails
from .filter_order import filter_order
from django.views.generic import ListView

User = get_user_model()


class OrderListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "dashboard/order/order_list.html"
    context_object_name = "object_list"

    def get_queryset(self):
        queryset = User.objects.select_related('cook').filter(
            cook__isnull=False, role__contains=[User.COOK])
        order_data = Order.objects.all().order_by('-created_at')
        cook_data = CookOrderDetails.objects.select_related(
            'order').filter(order__order_id__isnull=False)
        courier_data = CourierOrder.objects.select_related(
            'order').filter(order__order_id__isnull=False)
        q = self.request.GET.get('q')
        status = self.request.GET.getlist('status')
        if q is not None:
            queryset = queryset.filter(
                Q(username__icontains=q) | Q(mobile_number__icontains=q))
        if status:
            queryset = User.objects.filter(status__in=status)
        if status:
            context = filter_order(queryset, status)
        else:
            context = {
                "queryset": queryset,
                "all_order": "checked",
                "In": "",
                "En": "",
                "Delivered": ""
            }
        context = {
            'order_data': order_data,
            'cook_data': cook_data,
            'courier_data': courier_data,
        }
        return context

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['order_active'] = True
        return context


class OrderDetailsView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = "dashboard/order/order_details_view.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        order_details = OrderMenuItem.objects.get(order__id=pk)
        cook_details = CookOrderDetails.objects.get(order__id=pk)
        courier_details = CourierOrder.objects.get(order__id=pk)
        context = super(OrderDetailsView, self).get_context_data(**kwargs)
        context = {
            'order_active': True,
            'order_details': order_details,
            'cook_details': cook_details,
            'courier_details': courier_details,
        }
        return context


class OrderView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/order/order_details.html"

    def get_context_data(self, **kwargs):
        temp = None
        pk = self.kwargs.get('pk')
        order_data = OrderMenuSubItem.objects.filter(id=pk)
        for i in order_data:
            temp = i.order_menu_item.order.order_id
        context = super(OrderView, self).get_context_data(**kwargs)
        courier_data = CourierOrder.objects.filter(order__order_id=temp)

        context = {
            'customer_active': True,
            'order_data': order_data,
            'courier_data': courier_data,
        }
        return context
