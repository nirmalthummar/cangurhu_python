from django.contrib import admin
from apps.order.models import Order, OrderMenuItem, OrderMenuSubItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'customer', 'customer_address', 'cook_address', 'status', 'tip_amount', 'tip_type', 'shipping', 'sub_total', 'total', 'grand_total', 'amount_paid', 'distance')


admin.site.register(Order, OrderAdmin)


class OrderMenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'menu_item', 'quantity', 'price')


admin.site.register(OrderMenuItem, OrderMenuItemAdmin)


class OrderMenuSubItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'menu_sub_item', 'order_menu_item', 'price')


admin.site.register(OrderMenuSubItem, OrderMenuSubItemAdmin)
