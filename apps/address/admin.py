from django.contrib import admin
from .models import Address, AddressCategory, AddCard


class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'house_no', 'state', 'country_id', 'user_id', 'zipcode', 'town', 'address_type', 'address_category', 'is_default')


admin.site.register(Address, AddressAdmin)


class AddressCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')


admin.site.register(AddressCategory, AddressCategoryAdmin)

admin.site.register(AddCard)
