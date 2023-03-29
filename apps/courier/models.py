from django.db import models

from apps.order.models import Order
from apps.snippets.models import Country
from core.models import TimestampedModel
from core.utils import upload_path_handler, generate_sequence


class Courier(TimestampedModel):
    """
    Cook number is a 14 digits alphanumeric code.
    Example: USDLAA10008015
    First 2 digits: ISO-code of the COUNTRY where the customer, restaurant or driver is located it.
                    example: US, CA, MX,UK, FR, RU, etc..
    Next 2 digits: Stakeholder’s type:
                    CT: Customer
                    RS: Restaurant / Cook
                    DL: Courier / Delivery
    Next 10 digits: 10 DIGITS sequential number
    """

    INITIAL = 'initial'
    PENDING = 'pending'
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    STATUS_CHOICES = (
        (INITIAL, 'Initial'),
        (PENDING, 'Pending'),
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive')
    )

    MOTORBIKE = 'motorbike'
    BIKE = 'bike'
    BY_FOOT = 'by_foot'

    VEHICLE_TYPES_CHOICES = (
        (MOTORBIKE, 'Motorbike'),
        (BIKE, 'Bike'),
        (BY_FOOT, 'By Foot')
    )

    courier_id = models.CharField(max_length=14, unique=True, null=True, blank=True)
    user = models.OneToOneField(
        'accounts.User',
        related_name='courier',
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    country = models.ForeignKey(
        Country,
        db_column='country_id',
        related_name='courier_country',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    dob = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_path_handler, null=True, blank=True)
    work_permit = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    driving_licence = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    govt_cert = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    contract_signature = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    e_signed_contract = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    vehicle_type = models.CharField(max_length=11, choices=VEHICLE_TYPES_CHOICES, null=True, blank=True)
    vehicle_registration = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    vehicle_insurance = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=INITIAL)

    class Meta:
        db_table = 'table_courier'

    def save(self, *args, **kwargs):
        if self.courier_id is None and self.country:
            country_iso = self.country.iso2
            holder_type = 'DL'
            last_courier = Courier.objects.filter(courier_id__isnull=False).last()
            if last_courier:
                last_courier_id = last_courier.courier_id[4:]
                self.courier_id = generate_sequence(country_iso, holder_type, last_courier_id)
            else:
                self.courier_id = generate_sequence(country_iso, holder_type)
        super(Courier, self).save(*args, **kwargs)

    def __str__(self):
        if self.courier_id:
            return self.courier_id
        return self.user.username


class CourierOrder(TimestampedModel):
    PENDING = 'PE'
    ACCEPTED_BY_COURIER = 'ACR'
    CANCELED_BY_COURIER = 'CCR'
    PICKED_UP = 'PIU'
    ON_THE_WAY = 'OTW'
    DELIVERED = 'DE'

    COURIER_ORDER_STATUS_CHOICES = (
        (PENDING, "pending"),
        (ACCEPTED_BY_COURIER, 'courier accepted order'),
        (CANCELED_BY_COURIER, 'courier canceled order'),
        (PICKED_UP, 'picked up'),
        (ON_THE_WAY, 'on the way'),
        (DELIVERED, 'delivered'),

    )
    courier_order_id = models.BigAutoField(primary_key=True, editable=False)
    courier = models.ForeignKey(Courier,
                                related_name="courier_order",
                                on_delete=models.CASCADE,
                                db_column='courier_id',
                                null=True, blank=True)
    order = models.ForeignKey(Order,
                              related_name="courier_order_id",
                              on_delete=models.CASCADE,
                              db_column='order_id',
                              null=True, blank=True
                              )
    courier_status = models.CharField(max_length=25, choices=COURIER_ORDER_STATUS_CHOICES, default=PENDING)
    eta = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    reason = models.CharField(max_length=120, null=True, blank=True)
    total_distance = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    earnings = models.DecimalField(max_digits=19, decimal_places=2, default=0)


class NewCourierTrainingDocument(TimestampedModel):
    file_name = models.CharField(max_length=255, null=True, blank=True)
    document_file = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
