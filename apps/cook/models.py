from pickle import APPEND
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.snippets.models import Country
from core.models import TimestampedModel
from core.constant import ACTIVE, STATUS_CHOICES
from core.utils import upload_path_handler, generate_sequence, generate_item_sequence



class Cook(TimestampedModel):
    """
    Cook number is a 14 digits alphanumeric code.
    Example: USRSAA10008015
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

    cook_id = models.CharField(max_length=14, unique=True, null=True, blank=True)
    user = models.OneToOneField(
        'accounts.User',
        related_name='cook',
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    country = models.ForeignKey(
        Country,
        db_column='country_id',
        related_name='cook_country',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    dob = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_path_handler, null=True, blank=True)
    work_permit = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    govt_cert = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    insurance_cert = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    medical_clearance = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    food_cert = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    featured_cook = models.BooleanField(default=False)
    top_cook = models.BooleanField(default=False)
    near_by_cook = models.BooleanField(default=False)
    total_review = models.IntegerField(null=True, blank=True, default=0)     #count of ratings
    avg_star_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True,
                                                  null=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=INITIAL)

    class Meta:
        db_table = 'table_cook'

    def save(self, *args, **kwargs):
        print(self.created_at)
        if self.cook_id is None and self.country:
            country_iso = self.country.iso2
            holder_type = 'RS'
            last_cook = Cook.objects.filter(cook_id__isnull=False).last()
            if last_cook:
                last_cook_id = last_cook.cook_id[4:]
                self.cook_id = generate_sequence(country_iso, holder_type, last_cook_id)
            else:
                self.cook_id = generate_sequence(country_iso, holder_type)
        super(Cook, self).save(*args, **kwargs)

    def __str__(self):
        if self.cook_id:
            return self.cook_id
        return self.user.username


class KitchenPremises(TimestampedModel):
    document_id = models.BigAutoField(primary_key=True, editable=False)
    kitchen_premises = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    cook = models.ForeignKey(
        Cook,
        related_name='kitchen_premises',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.document_id} - {self.cook.user.username}"


class MenuCategory(TimestampedModel):
    category_icon = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    category_name = models.CharField(max_length=50)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        db_table = 'table_menu_category'
        ordering = ['-id']

    def __str__(self):
        return self.category_name


class MenuItem(TimestampedModel):
    NONE = 'none'
    VEGETARIAN = 'vegetarian'
    KOSHER = 'kosher'
    HALAL = 'halal'
    GLUTEN_FREE = 'gulten_free'
    NUTS_FREE = 'nuts_free'

    WARNING_CHOICES = (
        (NONE, 'None'),
        (KOSHER, 'Kosher'),
        (HALAL, 'Halal'),
        (GLUTEN_FREE, 'Gluten Free'),
        (NUTS_FREE, 'Nuts Free')
    )

    cook = models.ForeignKey(
        Cook,
        related_name='cook_menu_item',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    category = models.ForeignKey(
        MenuCategory,
        related_name='menu_item_category',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    item_number = models.CharField(max_length=19, null=True, blank=True)
    title = models.CharField(max_length=120, help_text=_("Dish Title"))
    item_img = models.ImageField(upload_to=upload_path_handler, null=True, blank=True)
    size = models.JSONField(default=list)
    warning = models.CharField(max_length=12, choices=WARNING_CHOICES, default=None)
    prepare_time = models.IntegerField(help_text=_("Prepare time in minutes"))
    item_type = models.CharField(max_length=20)
    nutrition_info = models.TextField(null=True, blank=True)
    cultural_facts = models.TextField(null=True, blank=True)
    commercial_info = models.TextField(null=True, blank=True)
    total_like = models.IntegerField(null=True, blank=True, default=0)
    total_dislike = models.IntegerField(null=True, blank=True, default=0)
    total_review = models.IntegerField(null=True, blank=True, default=0)
    avg_star_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True,
                                                  null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        db_table = 'table_menu_items'
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def save(self, *args, **kwargs):
        if self.item_number is None:
            if self.cook and self.cook.cook_id is not None:
                last_item = MenuItem.objects.filter(item_number__isnull=False).last()
                if last_item:
                    if len(last_item.item_number) == 19:
                        last_item_number = last_item.item_number[14:]
                        self.item_number = generate_item_sequence(self.cook.cook_id, last_item_number)
                    else:
                        self.item_number = generate_item_sequence(self.cook.cook_id)
                else:
                    self.item_number = generate_item_sequence(self.cook.cook_id)
        super(MenuItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class MenuSubItem(TimestampedModel):
    title = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    prepare_time = models.IntegerField(help_text=_("Prepare time in minutes"))
    total_calories = models.DecimalField(max_digits=7, decimal_places=3)
    nutrition_info = models.TextField(null=True, blank=True)
    cultural_facts = models.TextField(null=True, blank=True)
    commercial_info = models.TextField(null=True, blank=True)
    menu_item = models.ForeignKey(
        MenuItem,
        related_name='menu_sub_items',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    class Meta:
        db_table = 'table_menu_sub_items'

    def __str__(self):
        return self.title


class FSCCatalogue(TimestampedModel):
    CS = 'CS'
    KM = 'KM'
    SF = 'SF'
    FH = 'FH'

    FSC_CATALOGUE_CHOICES = (
        (CS, 'CS'),
        (KM, 'KM'),
        (SF, 'SF'),
        (FH, 'FH')
    )

    INITIAL = 'initial'
    PASS = 'pass'
    FAIL = 'fail'

    STATUS_CHOICES = (
        (INITIAL, 'Initial'),
        (PASS, 'Pass'),
        (FAIL, 'Fail')
    )

    name = models.CharField(max_length=50)
    quantity = models.IntegerField(null=True, blank=True)
    fsc_type = models.CharField(max_length=10, choices=FSC_CATALOGUE_CHOICES, default=CS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=INITIAL)

    class Meta:
        db_table = 'table_food_compliance_safety'

    def __str__(self):
        return self.name


class FSCCatalogueImage(TimestampedModel):
    INITIAL = 'initial'
    PASS = 'pass'
    FAIL = 'fail'

    STATUS_CHOICES = (
        (INITIAL, 'Initial'),
        (PASS, 'Pass'),
        (FAIL, 'Fail')
    )

    image = models.ImageField(upload_to=upload_path_handler, null=True, blank=True)
    fsc_catalogue = models.ForeignKey(
        FSCCatalogue,
        related_name='fsc_catalogue_images',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    cook = models.ForeignKey(
        Cook,
        related_name='fsc_catalogue_cook',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    feedback = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=INITIAL)

    class Meta:
        db_table = 'table_food_compliance_images'

    def __str__(self) -> str:
        print(self.cook)
        return str(self.cook)


class CookOrderDetails(TimestampedModel):
    PENDING = 'PE'
    ACCEPTED_BY_COOK = 'ACK'
    CANCELED_BY_COOK = 'CCK'
    COOKING_IN_PROGRESS = 'CP'
    READY = 'RE'
    READY_TO_PICKUP = 'REP'

    COOK_ORDER_STATUS_CHOICES = (
        (PENDING, "pending"),
        (ACCEPTED_BY_COOK, 'cook accepted order'),
        (CANCELED_BY_COOK, 'cook canceled order'),
        (COOKING_IN_PROGRESS, "cooking in progress"),
        (READY, 'ready'),
        (READY_TO_PICKUP, "ready to pickup"),
    )

    from apps.order.models import Order
    cook_order_id = models.BigAutoField(primary_key=True, editable=False)
    cook = models.ForeignKey(Cook,
                             related_name="cook_order",
                             on_delete=models.CASCADE,
                             db_column='cook_id',
                             null=True, blank=True)
    order = models.ForeignKey(Order,
                              related_name="cook_order",
                              on_delete=models.CASCADE,
                              db_column='order_id',
                              null=True, blank=True)
    cook_status = models.CharField(max_length=25, choices=COOK_ORDER_STATUS_CHOICES, default=PENDING)
    eta = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    reason = models.CharField(max_length=120, null=True, blank=True)
    is_future_order = models.BooleanField(default=False)
    order_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'table_cook_order_details'
