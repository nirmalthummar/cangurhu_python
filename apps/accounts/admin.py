from django.contrib import admin

from .models import User, StoreToken, StripeCustomerUser, BankAccount


class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'isd_code', 'mobile_number', 'role', 'is_staff', 'is_active', 'status')


admin.site.register(User, UserAdmin)


class StoreTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'device_type', 'device_token')


admin.site.register(StoreToken, StoreTokenAdmin)


class StripeCustomerUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'stripe_customer_id', 'active')


admin.site.register(StripeCustomerUser, StripeCustomerUserAdmin)


class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'country', 'bank_name', 'account_no', 'account_holder_name', 'bank_ifsc_code')

admin.site.register(BankAccount, BankAccountAdmin)
