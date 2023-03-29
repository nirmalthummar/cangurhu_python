from django.urls import path
from .views import (
    CartAPIView,
    CartItemAPIView,
    CartItemUpdateAPIView,
    CartItemRemoveAPIView,
    MoveToCartView,
    CartItemView,
    CartItemAV,
)

app_name = 'cart'
urlpatterns = [
    path('', CartAPIView.as_view(), name='cart'),
    path('item/', CartItemAPIView.as_view(), name='cart-item'),
    path('item/<int:pk>/update/', CartItemUpdateAPIView.as_view(), name='cart-item-update'),
    path('item/<int:cart_menu_item_id>/move/', MoveToCartView.as_view(), name='cart-item-move'),
    path('item/<int:pk>/delete/', CartItemRemoveAPIView.as_view(), name='cart-item-remove'),

    path('item/add/', CartItemAV.as_view(), name='cart-item-add'),

    # path('new/add/', CartItemView.as_view(), name='cart-item-add'),
]
