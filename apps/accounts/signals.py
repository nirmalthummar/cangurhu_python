from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.cart.models import Cart
from apps.cook.models import Cook
from apps.courier.models import Courier
from apps.customer.models import Customer

User = get_user_model()


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    if instance:
        if instance.last_role == User.CUSTOMER:
            instance.customer, __ = Customer.objects.get_or_create(user=instance)
            __, __ = Cart.objects.get_or_create(customer=instance.customer)

        if instance.last_role == User.COOK:
            instance.cook, __ = Cook.objects.get_or_create(user=instance)

        if instance.last_role == User.COURIER:
            instance.courier, __ = Courier.objects.get_or_create(user=instance)
