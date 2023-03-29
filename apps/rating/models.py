from django.db import models
from core.models import TimestampedModel
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.cook.models import Cook
from apps.customer.models import Customer
from apps.cook.models import MenuItem
from apps.courier.models import Courier


class CookFeedback(TimestampedModel):

    customer = models.ForeignKey(
        Customer,
        related_name="cook_rating_customer",
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    cook = models.ForeignKey(
        Cook,
        related_name='cook_rating',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    courier_user = models.ForeignKey(
        Courier,
        related_name='courier_rating',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    star_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.CharField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer.user.username} feedback to "

    class Meta:
        db_table = "table_cook_feedback"
        unique_together = (("customer", "cook"),)


class DishGrade(TimestampedModel):

    BAD = 1
    OKAY = 2
    GOOD = 3
    VERY_GOOD = 4

    FEEDBACK_CHOICES = (
        (BAD, "bad"),
        (OKAY, "okay"),
        (GOOD, "good"),
        (VERY_GOOD, "very good"),
    )

    customer = models.ForeignKey(
        Customer,
        related_name="dish_grade_customer",
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    menu_item = models.ForeignKey(
        MenuItem,
        related_name="dish_grade_menu_item",
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    star_rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    like = models.PositiveIntegerField(default=0, blank=True, null=True)
    dislike = models.PositiveIntegerField(default=0, blank=True, null=True)
    taste = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], blank=True, null=True)
    use_of_ingredients = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], blank=True, null=True)
    presentation = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer.user.username} feedback to menu item {self.menu_item.title}"

    class Meta:
        db_table = "table_dish_grade"
