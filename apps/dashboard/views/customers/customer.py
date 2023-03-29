import collections
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from apps.cook.models import Cook
from apps.courier.models import CourierOrder
from .filter_customer import filter_customer
from apps.order.models import *
from apps.address.models import *

User = get_user_model()


class CustomerListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "dashboard/customer/customer_list.html"
    context_object_name = "object_list"

    def get_queryset(self):
        queryset = User.objects.select_related('customer').filter(
            customer__isnull=False, role__contains=[User.CUSTOMER]).order_by('-created_at')
        q = self.request.GET.get('q')
        # # status = self.request.GET.get('status')
        status = self.request.GET.getlist('status')
        if q is not None:
            queryset = queryset.filter(
                Q(username__icontains=q) | Q(mobile_number__icontains=q))
        if status:
            queryset = User.objects.filter(status__in=status)
        if status:
            context = filter_customer(queryset, status)
        else:
            context = {
                "queryset": queryset,
                "all": "checked",
                "blocked": "",
                "active": "",
                "registered": ""
            }

        return context
        # return queryset

    def get_context_data(self, **kwargs):
        context = super(CustomerListView, self).get_context_data(**kwargs)
        context['customer_active'] = True
        return context


def customer_status(request, action, pk):
    INACTIVE = 'inactive'
    ACTIVE = 'active'
    customer = Customer.objects.get(user__user_id=pk)

    if action == "activate":
        customer.status = ACTIVE
        URL = '/Dashboard/Customers/'
    elif action == "activateID":
        customer.status = ACTIVE
        URL = f'/Dashboard/Customers/{pk}'
    elif action == "deactivate":
        customer.status = INACTIVE
        URL = '/Dashboard/Customers/'
    elif action == "deactivateID":
        customer.status = INACTIVE
        URL = f'/Dashboard/Customers/{pk}'
    customer.save()
    return redirect(URL)


class CustomerDetailView(DetailView):
    model = User
    template_name = "dashboard/customer/customer_detail.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        customer_data = User.objects.filter(user_id=pk)
        customer_address_data = Address.objects.filter(user_id=pk)
        order_data = OrderMenuSubItem.objects.filter(
            order_menu_item__order__customer__user__user_id=pk)
        courier_data = CourierOrder.objects.filter(
            order__customer__user__user_id=pk)

        context = {
            'customer_active': True,
            'customer_data': customer_data,
            'customer_address_data': customer_address_data,
            'order_data': order_data,
            'courier_data': courier_data,
        }
        return context


class CommunicateDetailView(DetailView):
    model = User
    template_name = "dashboard/communicate.html"
    # queryset = User.objects.select_related('customer').filter(role__contains=[User.CUSTOMER])
    queryset = User.objects.select_related('customer')

    def get_context_data(self, **kwargs):
        context = super(CommunicateDetailView, self).get_context_data(**kwargs)
        context['customer_active'] = True
        context['iter'] = isinstance(context['user'], collections.Iterable)
        return context
