from django.contrib import admin

from apps.notification.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'is_read', 'is_deleted')


admin.site.register(Notification, NotificationAdmin)
