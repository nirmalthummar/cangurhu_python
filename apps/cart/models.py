from django.contrib.auth import get_user_model
from django.db import models

from apps.customer.models import Customer
from apps.cook.models import MenuItem, MenuSubItem
from core.models import TimestampedModel

User = get_user_model()


class Cart(TimestampedModel):
    customer = models.OneToOneField(
        Customer,
        related_name="cart",
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    count = models.PositiveIntegerField(default=0)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    class Meta:
        db_table = "table_cart"

    def __str__(self):
        print("inside cart model")
        return "Customer: {} has {} items in their cart. Their total is ${}".format(
            self.customer, self.count, self.total
        )


class CartMenuItem(TimestampedModel):
    menu_item = models.ForeignKey(
        MenuItem,
        related_name="cart_menu_item",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    cart = models.ForeignKey(
        Cart,
        related_name="cart_menu",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    quantity = models.JSONField(default=list)
    is_future_order = models.BooleanField(default=False)
    save_for_later = models.BooleanField(default=False)
    order_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "table_cart_menu_item"

    def __str__(self):
        return "This entry contains {} {}(s).".format(self.quantity, self.menu_item.title)

    @property
    def cook_name(self):
        if self.menu_item:
            return self.menu_item.cook.user.username
        return ""

    def menu_item_name(self):
        if self.menu_item:
            return self.menu_item.title
        return ""

    @property
    def cook_id(self):
        if self.menu_item:
            return self.menu_item.cook.cook_id
        return ""


class CartMenuSubItem(TimestampedModel):
    cart_menu_item = models.ForeignKey(
        CartMenuItem,
        related_name="cart_sub_menu",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    sub_menu_item = models.ForeignKey(
        MenuSubItem,
        related_name="cart_sub_menu_items",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "table_cart_sub_menu_items"

    def __str__(self):
        return "This entry contains {} {}(s).".format(self.quantity, self.sub_menu_item)
