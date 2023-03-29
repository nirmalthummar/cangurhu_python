from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class Verification(models.Model):
    has_email_verified = models.BooleanField(
        default=False
    )
    has_mobile_verified = models.BooleanField(
        default=False
    )

    class Meta:
        abstract = True
