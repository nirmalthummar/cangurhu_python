from django.urls import path
from .views import (
    CookAPIView,
    CookDetailAPIView,
    CookFSCDataAPIView,
    MenuCategoryListAPIView,
    MenuItemListCreateAPIView,
    MenuItemRetrieveUpdateDestroy,
    TopDishesAPIView,
    TopCookAPIView,
    FeaturedCookAPIView,
    NearByCookAPIView,
    OfferZoneCookAPIView,

    CookSearchAPIView,
    FSCCatalogueAPIView,
    FSCCatalogueImageAPIView,
    FSC,
    FSCCatalogueImageAPIView,
    CookOrderPlaceView, CookOrderView, CookAgreeFutureOrderAPIView, CookingInProgressListView, CookPastOrderListView, CookOrderStatusToCooking,
    OrderReadyToPickup, ReadyToPickupListView, CookFutureOrderPlaceView, MenuCategoryView, MenuCategoryDetail, MenuItemListCreateAV, MenuItemDetailAV
)

from apps.rating.api.views import CookFeedbackView, CookFeedbackDetailView, DishGradeView

from apps.rating.api.views import CookFeedbackView

app_name = 'cook'
urlpatterns = [
    path('', CookAPIView.as_view(), name='cook'),

    path('fscdata', CookFSCDataAPIView.as_view(), name='cook-fsc'),

    path('menu/category/', MenuCategoryListAPIView.as_view(), name='menu-category'),
    path('menu/items/', MenuItemListCreateAPIView.as_view(), name='menu-item'),
    path('menu/items/<int:pk>/', MenuItemRetrieveUpdateDestroy.as_view(), name='menu-item-detail'),

    path('top-dishes', TopDishesAPIView.as_view(), name='top-dishes'),
    path('top-cooks', TopCookAPIView.as_view(), name='top-cook'),
    path('featured-cooks', FeaturedCookAPIView.as_view(), name='featured-cook'),
    path('near-by-cooks', NearByCookAPIView.as_view(), name='near-by-cook'),
    path('offer-zone', OfferZoneCookAPIView.as_view(), name='offer-zone'),

    path('menu/item/', MenuItemListCreateAV.as_view(), name='menu-item'),  #Testing APIView
    path('menu/item/<int:pk>/', MenuItemDetailAV.as_view(), name='menu-item-detail'),  #Testing APIView

    # Menu Item Feedback
    path('menu/items/<int:menu_item_id>/rate', DishGradeView.as_view(), name='dish-feedback'),

    path('<str:cook_id>/rate/', CookFeedbackView.as_view(), name='cook-feedback'),

    path('search', CookSearchAPIView.as_view(), name='cook-search'),

    path('fsc/catalogue/', FSCCatalogueAPIView.as_view(), name="fsc-food-catalogue"),
    path('fsc/catalogue/images/', FSCCatalogueImageAPIView.as_view(), name="fsc-food-catalogue-image"),
    path('fsc/catalogue/images/<int:id>/', FSCCatalogueImageAPIView.as_view(), name="fsc-food-catalogue-image-patch"),

    # ORDER

    path('new-order-placed/', CookOrderPlaceView.as_view(), name="cook-order-placed"),
    path('new-future-order-placed/', CookFutureOrderPlaceView.as_view(), name="cook-future-order-placed"),
    path('new-future-order-placed/detail/<str:order>/', CookFutureOrderPlaceView.as_view(), name="cook-future-order-placed"),
    path('new-order-placed/detail/<str:order_id>/', CookOrderPlaceView.as_view(), name="cook-order-placed-detail"),
    path('new-future-order/<str:id>/agree/', CookAgreeFutureOrderAPIView.as_view(), name="cook-future-order-placed"
                                                                                         "-detail"),
    path('cook-order/<str:order_id>/status/', CookOrderView.as_view(), name="cook-order-status"),
    path('start-cooking-order/<str:order_id>/status/', CookOrderStatusToCooking.as_view(), name="cook-order-status-start-cooking"),
    path('order-cooking-in-progress/', CookingInProgressListView.as_view(), name="cook-order-cooking-in-progress"),
    path('order-cooking-in-progress/order-detail/<str:order_id>/', CookingInProgressListView.as_view(),
                                                                            name="cook-order-cooking-in-progress-detail"),
    path('order-ready-to-pickup/<str:order_id>/status/', OrderReadyToPickup.as_view(),
                                                                            name="cook-order-status-ready-to-pickup"),
    path('order-ready-to-pickup/list/', ReadyToPickupListView.as_view(),
                                                                        name="cook-order-ready-to-pickup-list"),
    path('order-ready-to-pickup/order-detail/<str:order_id>/', ReadyToPickupListView.as_view(),
                                                                        name="cook-order-ready-to-pickup-order-detail"),

    path('cook-past-order/', CookPastOrderListView.as_view(), name='courier-past-order'),
    path('cook-past-order/detail/<str:order_id>/', CookPastOrderListView.as_view(), name='courier-past-order'),
    path('<str:cook_id>/', CookDetailAPIView.as_view(), name='cook-detail'),


    path('fsc/catalogue/upload/', FSC.as_view(), name="fsc-upload"),


    path('menu/item/category/', MenuCategoryView.as_view(), name='menu-category'),
    path('menu/item/category/<int:pk>/', MenuCategoryDetail.as_view(), name='menu-item-category'),

]