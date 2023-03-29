from django.urls import path
from apps.order.api.views import (

    OrderView, OrderMenuItemView, ReOrderAPIView, FutureOrderAPIView, PushDataToRedis)

app_name = 'order'

urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('future-order', FutureOrderAPIView.as_view(), name='order'),
    path('detail/<str:id>/', OrderView.as_view(), name='order-detail'),
    path('reorder/', ReOrderAPIView.as_view(), name='reorder'),
    path('menu-item/', OrderMenuItemView.as_view(), name='order_menu_item'),
    path('push/', PushDataToRedis.as_view(), name='push-data'),
]
