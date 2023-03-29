from django.urls import path
from .views import (
    AddressAPIView,
    AddressDetailView,
    AddressCategoryView,
    AddressAV,
    AddressDetailAV,
    AddCardAPIView,
    AddCardDetail,
    CookAPIView,
    CookDetailAPI,
    OrderAPIView,
    OrderUpdateAPIView,
    CookOrderAPIView,
    CourierOrderAPIView
)

app_name = 'address'
urlpatterns = [
    path('', AddressAPIView.as_view(), name='address'),
    path('<int:address_id>', AddressDetailView.as_view(), name='address-detail'),
    path('category', AddressCategoryView.as_view(), name='address_category'),
    path('add/<int:pk>', AddressDetailAV.as_view(), name='address-detail'),#testing purpose
    path('add/', AddressAV.as_view(), name='address'),#testing purpose
    path('addcard/', AddCardAPIView.as_view(), name='addcard'),#testing purpose
    path('addcard/<int:pk>', AddCardDetail.as_view(), name='addcard-detail'),#testing
    path('cook/', CookAPIView.as_view(), name='cook-detail'),#testing
    path('cook/<int:pk>', CookDetailAPI.as_view(), name='cook-details'),#testing
    path('order/', OrderAPIView.as_view(), name='order-detail'),#testing
    path('order/<int:pk>', OrderUpdateAPIView.as_view(), name='order-update-detail'),#testing
    path('order/menu-item', OrderUpdateAPIView.as_view(), name='order-update-detail'),#testing
    path('cook-order/<int:order_id>', CookOrderAPIView.as_view(), name='cook-order-detail'),#testing
    path('courier-order/<int:order_id>', CourierOrderAPIView.as_view(), name='courier-order-detail'),#testing

]