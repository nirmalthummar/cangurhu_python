from django.db import models
from django.contrib.auth import get_user_model
from core.models import TimestampedModel

from apps.snippets.models import Country
from apps.cook.models import Cook, MenuCategory


User = get_user_model()


class AddressCategory(TimestampedModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'table_address_category'


class Address(TimestampedModel):
    HOME = 'home'
    OFFICE = 'office'
    OTHER = 'other'

    ADDRESS_CHOICES = (
        (HOME, 'Home'),
        (OFFICE, 'Office'),
        (OTHER, 'Other')
    )

    COMMUNICATION_SHARED_COURTYARD = 'CSC'
    CUBICLE = 'CBC'
    HACIENDA_FARM = 'HCF'
    HOUSE_DETACHED = 'HDD'
    HOUSE_SEMI_DETACHED = 'HSD'
    OFFICE_COMMERCIAL_MALL = 'OCM'
    OFFICE_BUILDING = 'OFB'
    OPEN_AIR_PARK = 'OAP'
    PLANT_WAREHOUSE = 'PWH'
    RESIDENTIAL_BUILDING = 'RSB'
    RESIDENTIAL_CONDOMINIUM = 'RSC'

    ADDRESS_CATEGORY_CHOICES = (
        (COMMUNICATION_SHARED_COURTYARD, 'Communication Shared Courtyard'),
        (CUBICLE, 'Cubicle'),
        (HACIENDA_FARM, 'Hacienda / Farm'),
        (HOUSE_DETACHED, 'House Detached'),
        (HOUSE_SEMI_DETACHED, 'House Semi-Detached'),
        (OFFICE_COMMERCIAL_MALL, 'Office or Commercial Mall'),
        (OFFICE_BUILDING, 'Office Building'),
        (OPEN_AIR_PARK, 'Open Air / Park'),
        (PLANT_WAREHOUSE, 'Plant / Warehouse'),
        (RESIDENTIAL_BUILDING, 'Residential Building'),
        (RESIDENTIAL_CONDOMINIUM, 'Residential Condominium')
    )

    address_id = models.BigAutoField(primary_key=True, editable=False)
    house_no = models.CharField(max_length=120)
    state = models.CharField(max_length=50, null=True, blank=True)
    country_id = models.ForeignKey(Country,
                                   on_delete=models.SET_NULL,
                                   db_column='country_id',
                                   related_name='country_address',
                                   null=True, blank=True)
    user_id = models.ForeignKey(User,
                                related_name='user_address',
                                on_delete=models.SET_NULL,
                                db_column='user_id',
                                blank=True, null=True)
    zipcode = models.CharField(max_length=11, null=True, blank=True)
    landmark = models.CharField(max_length=110, null=True, blank=True)
    town = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.CharField(max_length=15, null=True, blank=True)
    longitude = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=110, null=True, blank=True)
    address_type = models.CharField(max_length=110, choices=ADDRESS_CHOICES, null=True, blank=True)
    address_category = models.CharField(max_length=110, choices=ADDRESS_CATEGORY_CHOICES, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_id}"

    class Meta:
        db_table = 'table_address'


class AddCard(models.Model):
    cardholder_name = models.CharField(max_length=200)
    card_number = models.IntegerField()
    expiry_date = models.CharField(max_length=10)
    cvv = models.CharField(max_length=3)
    save_card = models.BooleanField(default=False)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="card_user",
                             )


    def __str__(self):
        return f"{self.cardholder_name}"
