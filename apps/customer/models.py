from django.db import models



from apps.snippets.models import Country
from core.models import TimestampedModel
from core.utils import upload_path_handler, generate_sequence


class Customer(TimestampedModel):
    """
    Customer number is a 14 digits alphanumeric code.
    Example: USCTAA10008015

    First 2 digits: ISO-code of the COUNTRY where the customer,
                    restaurant or driver is located it.
                    example: US, CA, MX,UK, FR, RU, etc..
    Next 2 digits: Stakeholder’s type:
                    CT: Customer
                    RS: Restaurant / Cook
                    DL: Courier / Delivery
    Next 10 digits: 10 DIGITS sequential number
    """

    PENDING = 'pending'
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive')
    )

    customer_id = models.CharField(max_length=14, unique=True, null=True, blank=True)
    user = models.OneToOneField(
        'accounts.User',
        related_name='customer',
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    country = models.ForeignKey(
        Country,
        db_column='country_id',
        related_name='customer_country',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    dob = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_path_handler, null=True, blank=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        db_table = 'table_customer'

    def save(self, *args, **kwargs):
        if self.customer_id is None and self.country:
            country_iso = self.country.iso2
            holder_type = 'CT'
            last_customer = Customer.objects.filter(customer_id__isnull=False).last()
            if last_customer:
                last_customer_id = last_customer.customer_id[4:]
                self.customer_id = generate_sequence(country_iso, holder_type, last_customer_id)
            else:
                self.customer_id = generate_sequence(country_iso, holder_type)
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        if self.customer_id:
            return self.customer_id
        return self.user.username


class CustomerOrder(TimestampedModel):

    PENDING = 'PE'
    CANCELED_BY_CUSTOMER = 'CCU'

    CUSTOMER_ORDER_STATUS_CHOICES = (
        (PENDING, "pending"),
        (CANCELED_BY_CUSTOMER, 'customer canceled order'),


    )
    # from apps.order.models import Order
    courier_order_id = models.BigAutoField(primary_key=True, editable=False)
    customer = models.ForeignKey(Customer,
                                 related_name="customer_order_status",
                                 on_delete=models.CASCADE,
                                 # db_column='customer_id',
                                 null=True, blank=True)
    order = models.ForeignKey('order.Order',
                              related_name="customer_order_status",
                              on_delete=models.CASCADE,
                              # db_column='customer_id',
                              null=True, blank=True
                              )
    customer_status = models.CharField(max_length=25, choices=CUSTOMER_ORDER_STATUS_CHOICES, default=PENDING)
    reason = models.CharField(max_length=120, null=True, blank=True)
