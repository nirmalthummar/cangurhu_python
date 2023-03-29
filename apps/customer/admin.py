from django.contrib import admin
from apps.customer.api.views import Customer
from apps.customer.models import CustomerOrder


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_id', 'user', 'country', 'dob', 'image', 'status')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerOrder)
