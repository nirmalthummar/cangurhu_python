from django.db import models
from core.models import TimestampedModel
from core.utils import default_key, upload_path_handler


# Country - India
class Country(TimestampedModel):
    country_id = models.BigAutoField(primary_key=True, editable=False)
    country_name = models.CharField(max_length=120, null=True)
    iso2 = models.CharField(max_length=2, null=True)
    iso3 = models.CharField(max_length=3, null=True)
    isd_code = models.CharField(max_length=20, null=True, blank=True)
    currency = models.CharField(max_length=4, null=True, blank=True)
    latitude = models.CharField(max_length=15, null=True, blank=True)
    longitude = models.CharField(max_length=15, null=True, blank=True)
    flag=models.ImageField(upload_to=upload_path_handler,null=True,blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "table_country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.country_name


# State - India -> Delhi
class State(TimestampedModel):
    state_id = models.BigAutoField(primary_key=True, editable=False)
    state_name = models.CharField(max_length=120, null=True)
    state_code = models.CharField(max_length=20, null=True, blank=True)
    country_id = models.ForeignKey(Country,
                                   on_delete=models.CASCADE,
                                   db_column='country_id',
                                   related_name='country_states',
                                   null=True, blank=True)
    latitude = models.CharField(max_length=15, null=True, blank=True)
    longitude = models.CharField(max_length=15, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "table_states"
        verbose_name_plural = "States"

    def __str__(self):
        return self.state_name


# City - India -> Delhi -> New Delhi
class City(TimestampedModel):
    city_id = models.BigAutoField(primary_key=True, editable=False)
    city_name = models.CharField(max_length=120, null=True)
    state_id = models.ForeignKey(State,
                                 on_delete=models.CASCADE,
                                 db_column='state_id',
                                 related_name='state_cities',
                                 null=True, blank=True)
    country_id = models.ForeignKey(Country,
                                   on_delete=models.CASCADE,
                                   related_name='country_cities',
                                   db_column='country_id',
                                   null=True,
                                   blank=True)
    latitude = models.CharField(max_length=15, null=True, blank=True)
    longitude = models.CharField(max_length=15, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "table_cities"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.city_name
