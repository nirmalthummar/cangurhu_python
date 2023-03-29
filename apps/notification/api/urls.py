from django.urls import path

from apps.notification.api.views import (NotificationDataView,
                                         )

app_name = 'notification'
urlpatterns = [

    path('list/', NotificationDataView.as_view(), name='notification'),
    path('detail/<int:id>/', NotificationDataView.as_view(), name='notification-detail'),
    path('delete/<int:id>/', NotificationDataView.as_view(), name='notification-delete-by-id'),
]
