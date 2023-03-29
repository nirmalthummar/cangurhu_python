from django.urls import path
from apps.courier.api.views import (
    CourierAPIView,
    CourierDocumentAPIView,
    CourierVehicleAPIView,
    CourierNewOrderListView,
    CourierOrderView,
    CourierPastOrderListView,
    CourierReadyToPickupList,
    CourierSetOrderPickedUpView,
    CourierSetOrderDeliveredView,
    CourierOrderCalculationView
)

app_name = 'courier'
urlpatterns = [
    path('', CourierAPIView.as_view(), name='courier'),
    path('document', CourierDocumentAPIView.as_view(), name='courier-document'),
    path('vehicle', CourierVehicleAPIView.as_view(), name='courier-vehicle'),
    path('new-order/', CourierNewOrderListView.as_view(), name='courier-neworder-list'),
    path('new-order/<str:order_id>/', CourierNewOrderListView.as_view(), name='courier-neworder-list'),
    path('courier-order/<str:order_id>/status/', CourierOrderView.as_view(), name='courier-order-status'),
    path('courier-ready-to-pickup/list/', CourierReadyToPickupList.as_view(), name='courier-ready-to-pickup-list'),
    path('courier-ready-to-pickup/detail/<str:order_id>/', CourierReadyToPickupList.as_view(),
         name='courier-ready-to-pickup-detail'),
    path('courier-order-picked-up/<str:order_id>/status/', CourierSetOrderPickedUpView.as_view(), name='courier-set-order-picked-up'),
    path('courier-order-delivered/<str:order_id>/status/', CourierSetOrderDeliveredView.as_view(), name='courier-set-order-delivered'),
    path('courier-past-order/', CourierPastOrderListView.as_view(), name='courier-past-order'),

    path('order/<int:courier_order_id>', CourierOrderCalculationView.as_view(), name='courier-order-calculation'),
]
