from datetime import datetime
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect

from apps.cook.models import Cook, FSCCatalogueImage, KitchenPremises, CookOrderDetails, MenuItem, MenuCategory
from apps.address.models import Address
from apps.courier.models import CourierOrder
from .filter_cook import filter_cook

User = get_user_model()

class CookListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "dashboard/cook/cook_list.html"
    context_object_name = "object_list"

    def get_queryset(self):
        queryset = User.objects.select_related('cook').filter(
            cook__isnull=False, role__contains=[User.COOK]).order_by('-created_at')
        fsc_data = FSCCatalogueImage.objects.select_related(
            'cook').filter(cook__isnull=False).order_by('-created_at')
        kitchen_premises_data = KitchenPremises.objects.select_related(
            'cook').filter(cook__isnull=False).order_by('-created_at')
        q = self.request.GET.get('q')
        status = self.request.GET.getlist('status')
        if q is not None:
            queryset = queryset.filter(
                Q(username__icontains=q) | Q(mobile_number__icontains=q))
        if status:
            queryset = User.objects.filter(status__in=status)
        if status:
            context = filter_cook(queryset, status)
        else:
            context = {
                "queryset": queryset,
                "all_cook": "checked",
                "pending_cook": "",
                "approved_cook": "",
                "pending_fsc": "",
                "approved_fsc": "",
                "fsc_data": fsc_data,
                "kitchen_premises_data": kitchen_premises_data,
            }


        return context

    def get_context_data(self, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        context['cook_approved_cook'] = True
        return context


def cook_status(request, action, pk):
    INACTIVE = 'inactive'
    ACTIVE = 'active'
    URL = f'/Dashboard/Cooks/{pk}'
    cook = Cook.objects.get(user__user_id=pk)

    if action == "activate":
        cook.status = ACTIVE
        URL = '/Dashboard/Cooks/'
    elif action == "activateID":
        cook.status = ACTIVE
        URL = f'/Dashboard/Cooks/{pk}'
    elif action == "deactivate":
        cook.status = INACTIVE
        URL = '/Dashboard/Cooks/'
    elif action == "deactivateID":
        cook.status = INACTIVE
        URL = f'/Dashboard/Cooks/{pk}'
    cook.save()
    return redirect(URL)


class CookDetailView(DetailView):
    model = User
    template_name = "dashboard/cook/cook_details.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        cook_data = Cook.objects.get(user__user_id=pk)
        cook_address = Address.objects.filter(user_id=pk)
        cook_order_data = CookOrderDetails.objects.filter(
            cook__user__user_id=pk)
        courier_order_data = {}
        for i in cook_order_data:
            courier_order_data[i.order.order_id] = CourierOrder.objects.get(
                order__order_id=i.order.order_id).courier.courier_id

        context = super(CookDetailView, self).get_context_data(**kwargs)
        context['cook_approved_cook'] = Cook
        user = self.get_object()

        # context['premises'] = user.cook.kitchen_premises.all()[:5]
        context = {
            'cook_order_data': cook_order_data,
            'cook_data': cook_data,
            'cook_address': cook_address,
            'courier_order_data': courier_order_data,
        }

        return context


class ViewCookMenuCatalog(DetailView):
    model = User
    template_name = "dashboard/menu-catalog.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        cook_name = User.objects.get(pk=pk).username
        menu_data = MenuItem.objects.filter(cook__user__user_id=pk)

        context = {
            'pk' : pk,
            'cook_name': cook_name,
            'menu_data': menu_data,
        }

        return context


class ViewFSC(DetailView):
    model = User
    template_name = "dashboard/cook-food-safety-compliance.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        cook_name = User.objects.get(pk=pk).username
        cook_data = Cook.objects.get(user__user_id=pk)
        try:
            fsc_data = FSCCatalogueImage.objects.filter(cook__user__user_id=pk)
        except FSCCatalogueImage.DoesNotExist:
            fsc_data = None

        context = {
            'cook_name': cook_name,
            'cook_data': cook_data,
            'fsc_data': fsc_data,

        }

        return context


class ViewCookRegView(DetailView):
    def get(self, request):

        user = User.objects.filter(role='{cook}').values()

        context = {
            'data': user,
            'cook_approved_cook': True

        }

        return render(request, "dashboard/view-cook-registration.html", context)


class ViewCookFSC(DetailView):
    def get(self, request):
        context = {
            'cook_approved_cook': True
        }
        return render(request, "dashboard/view-cook-cook-food-safety-compliance.html", context)


class ViewCookFSCResult(DetailView):
    def get(self, request):
        context = {
            'cook_approved_cook': True
        }
        return render(request, "dashboard/view-fsc-result.html", context)
