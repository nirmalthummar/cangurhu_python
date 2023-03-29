from django.db import models
from django.contrib.auth import get_user_model

from core.models import TimestampedModel

User = get_user_model()


class Notification(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=215, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'table_notification'
