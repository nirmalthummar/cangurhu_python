from django.db import models
from apps.address.models import Address
from apps.cook.models import MenuItem, MenuSubItem
from apps.customer.models import Customer
from core.models import TimestampedModel

ORDER_PLACED = 'OP'
PENDING = 'PE'
ACCEPTED_BY_COOK = 'ACK'
CANCELED_BY_COOK = 'CCK'
ACCEPTED_BY_COURIER = 'ACR'
CANCELED_BY_COURIER = 'CCR'
CANCELED_BY_CUSTOMER = 'CCU'
READY_TO_COOK = 'RCK'
COOKING_IN_PROGRESS = 'CP'
READY = 'RE'
READY_TO_PICKUP = 'REP'
PICKED_UP = 'PIU'
ON_THE_WAY = 'OTW'
DELIVERED = 'DE'

ORDER_STATUS_CHOICES = (
    (PENDING, 'pending'),
    (ORDER_PLACED, 'order placed'),
    (ACCEPTED_BY_COOK, 'cook accepted order'),
    (CANCELED_BY_COOK, 'cook canceled order'),
    (ACCEPTED_BY_COURIER, 'courier accepted order'),
    (CANCELED_BY_COURIER, 'courier canceled order'),
    (CANCELED_BY_CUSTOMER, 'customer canceled order'),
    (READY_TO_COOK, 'ready to cook'),
    (COOKING_IN_PROGRESS, 'cooking in progress'),
    (READY, 'ready'),
    (PICKED_UP, 'pickedup'),
    (ON_THE_WAY, 'on the way'),
    (DELIVERED, 'delivered')

)

PERCENTAGE = 'percentage'
AMOUNT = 'amount'
NONE = 'none'

TIP_TYPE_CHOICES = (
    (NONE, 'None'),
    (PERCENTAGE, 'Percentage'),
    (AMOUNT, 'Amount')
)

AMT_PENDING = 'pending'
SUCCEEDED = 'succeeded'
FAILED = 'failed'

AMOUNT_STATUS_CHOICES = (
    (AMT_PENDING, 'Pending'),
    (SUCCEEDED, 'Succeeded'),
    (FAILED, 'Failed')
)


class Order(TimestampedModel):
    order_id = models.CharField(max_length=18, unique=True, null=True, blank=True)
    customer = models.ForeignKey(
        Customer,
        related_name="customer_order",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    customer_address = models.ForeignKey(
        Address,
        related_name="customer_order_address",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    cook_address = models.ForeignKey(
        Address,
        related_name="cook_order_address",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    cook_instruction = models.TextField(null=True, blank=True)
    courier_instruction = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=ORDER_STATUS_CHOICES, default=PENDING)
    tip_amount = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    tip_type = models.CharField(max_length=11, choices=TIP_TYPE_CHOICES, default=NONE)
    sub_total = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    shipping = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    grand_total = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    amount_paid = models.CharField(max_length=25, choices=AMOUNT_STATUS_CHOICES, default=AMT_PENDING)
    payment_details = models.JSONField(null=True, blank=True)
    is_future_order = models.BooleanField(null=False, blank=False, default=False)
    order_date = models.DateField(null=True, blank=True)
    is_cook_agree = models.BooleanField(null=True, blank=True, default=False)
    distance = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        db_table = 'table_order'

    # def save(self, *args, **kwargs):
    #     if self.order_id is None:
    #         from datetime import datetime
    #         date = datetime.today().strftime('%Y%m%d')
    #         country_iso = self.customer.country.iso2
    #         last_order = Order.objects.all().exclude(id=self.id).last()
    #         if last_order:
    #             last_order_id = last_order.order_id[11:]
    #             self.order_id = generate_order_sequence(date, country_iso, last_order_id)
    #         else:
    #             self.order_id = generate_order_sequence(date, country_iso)
    #     super(Order, self).save(*args, **kwargs)

    # def __str__(self):
    #     if self.order_id:
    #         return self.order_id


class OrderMenuItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='customer_order_value',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    menu_item = models.ForeignKey(
        MenuItem,
        related_name='order_menu_item',
        on_delete=models.SET_NULL,
        null=True, blank=True)
    quantity = models.JSONField()
    price = models.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        db_table = 'table_order_menu_item'


class OrderMenuSubItem(models.Model):
    menu_sub_item = models.ForeignKey(
        MenuSubItem,
        related_name='menu_sub_item',
        on_delete=models.SET_NULL,
        null=True, blank=True)
    order_menu_item = models.ForeignKey(
        OrderMenuItem,
        related_name='order_menu_sub_item',
        on_delete=models.SET_NULL,
        null=True, blank=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        db_table = 'table_order_menu_sub_item'
