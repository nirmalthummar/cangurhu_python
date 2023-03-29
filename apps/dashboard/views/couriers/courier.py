from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from apps.courier.models import *
from apps.address.models import Address
from apps.config.models import HotZoneIncentivePercentage
from apps.order.models import OrderMenuSubItem

User = get_user_model()


class CourierListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "dashboard/courier/courier_list.html"
    context_object_name = "object_list"

    def get_queryset(self):
        queryset = User.objects.select_related('courier').filter(
            courier__isnull=False, role__contains=[User.COURIER]).order_by('-created_at')
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        vehicle = self.request.GET.get('vehicle')
        if q is not None:
            queryset = queryset.filter(
                Q(username__icontains=q) | Q(mobile_number__icontains=q))
        if status:
            queryset = queryset.filter(courier__status=status)
        if vehicle:
            queryset = queryset.filter(courier__vehicle_type=vehicle)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CourierListView, self).get_context_data(**kwargs)
        context['courier_active'] = True
        return context


def courier_status(request, action, pk):
    INACTIVE = 'inactive'
    ACTIVE = 'active'
    courier = Courier.objects.get(user__user_id=pk)

    if action == "activate":
        courier.status = ACTIVE
        URL = '/Dashboard/Couriers/'
    elif action == "activateID":
        courier.status = ACTIVE
        URL = f'/Dashboard/Couriers/{pk}'
    elif action == "deactivate":
        courier.status = INACTIVE
        URL = '/Dashboard/Couriers/'
    elif action == "deactivateID":
        courier.status = INACTIVE
        URL = f'/Dashboard/Couriers/{pk}'
    courier.save()
    return redirect(URL)


class CourierDetailView(DetailView):
    model = User
    template_name = "dashboard/courier/courier_details.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        courier_data = User.objects.filter(user_id=pk)
        courier_address_data = Address.objects.filter(user_id=pk)
        order_data = CourierOrder.objects.filter(
            courier__user__user_id=pk).order_by('-created_at')
        context = super(CourierDetailView, self).get_context_data(**kwargs)
        context = {
            'courier_active': True,
            'order_data': order_data,
            'courier_data': courier_data,
            'courier_address_data': courier_address_data,

        }
        return context


class ViewCourierInfo(DetailView):
    def get(self, request):
        context = {
            'courier_active': True
        }

        return render(request, "dashboard/view-admin-validates-courier-information.html", context)


class CourierOrderDetailView(DetailView):
    model = User
    template_name = "dashboard/courier-order-details.html"
    hot_zone = None
    country = None

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        courier_order_data = CourierOrder.objects.filter(courier_order_id=pk)
        for i in courier_order_data:
            country = i.courier.country
            order = i.order.order_id
        hot_zone = HotZoneIncentivePercentage.objects.filter(country=country)
        order_menu_data = OrderMenuSubItem.objects.filter(
            order_menu_item__order__order_id=order)
        context = {
            'courier_active': True,
            'courier_order_data': courier_order_data,
            'hot_zone': hot_zone,
            'order_menu_data': order_menu_data,
        }

        return context
