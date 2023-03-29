from django.urls import path
from apps.customer.api.views import (CustomerDetailView, CustomerCompletedOrderListView, CustomerCanceledOrderListView,
                                     CustomerOngoingOrderListView, CustomerOrderCancelStatusView)

app_name = 'customer'
urlpatterns = [
    path('', CustomerDetailView.as_view(), name='customer'),

    # customer order
    path('customer-order/<str:order_id>/status/', CustomerOrderCancelStatusView.as_view(), name="customer-order-cancel-status"),
    path('order/ongoing/', CustomerOngoingOrderListView.as_view(), name='customer completed order'),
    path('order/ongoing/<str:order_id>/', CustomerOngoingOrderListView.as_view(),
         name='customer completed order detail'),
    path('order/completed/', CustomerCompletedOrderListView.as_view(), name='customer completed order'),
    path('order/completed/<str:order_id>/', CustomerCompletedOrderListView.as_view(),
         name='customer completed order detail'),
    path('order/canceled/', CustomerCanceledOrderListView.as_view(), name='customer Canceled order'),
    path('order/canceled/<str:order_id>/', CustomerCanceledOrderListView.as_view(), name='customer Canceled order '),
]
