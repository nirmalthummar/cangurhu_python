from django.contrib import admin

from apps.cart.models import (
    Cart,
    CartMenuItem,
    CartMenuSubItem
)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'count', 'total')


admin.site.register(Cart, CartAdmin)


class CartMenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'menu_item', 'cart', 'quantity', 'is_future_order', 'save_for_later')


admin.site.register(CartMenuItem, CartMenuItemAdmin)


class CartMenuSubItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart_menu_item', 'sub_menu_item', 'quantity')


admin.site.register(CartMenuSubItem, CartMenuSubItemAdmin)
