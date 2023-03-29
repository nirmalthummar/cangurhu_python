from django.contrib.auth import get_user_model

from celery import shared_task


# @shared_task
def send_otp_on_mobile(user):
    from .models import VerificationDevice
    # User = get_user_model()
    #
    # user = User.objects.get(pk=user_id)
    device, __ = VerificationDevice.objects.get_or_create(
        user=user,
        mobile_number=user.mobile_number
    )

    token = device.generate_challenge()
    device.last_verified_counter = -1
    device.verified = False
    device.otp = token
    device.save()
    return token

