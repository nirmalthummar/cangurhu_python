from django.urls import path
from django.views.generic.base import TemplateView
from .views import *
from .views.forgotpassword import *
from .views.report.report import ReportListView
from .views.rating.rating import RatingListCourierView, RatingListCookView, RatingListView
from .views.central.all_app import NotificationListView, AllAppListView, OperationalKPIListView, AppConfigListView, AppConfigListViewUpdate, delete_item
from .views.customers.customer import CommunicateDetailView, customer_status
from .views.cooks.cook import ViewCookRegView, ViewFSC, ViewCookFSC, ViewCookMenuCatalog, ViewCookFSCResult, cook_status
from .views.couriers.courier import ViewCourierInfo, CourierOrderDetailView, courier_status
from django.conf import settings
from django.conf.urls.static import static

app_name = 'dashboard'
urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path('Login/', LoginView.as_view(), name='login'),
    path('Logout/', LogoutView.as_view(), name='logout'),

    path('ForgotPassword/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('ForgotPassword/OTPVerify/',
         ForgotPasswordVerifyView.as_view(), name='verify-otp'),

    path("Customers/", CustomerListView.as_view(), name="customers-list"),
    path("Customers/<int:pk>/", CustomerDetailView.as_view(),
         name="customers-detail"),
    path("Customer/Order/<int:pk>", OrderView.as_view(),
         name="customer-order-details"),
    path("customer_status/<str:action>/<int:pk>/", customer_status,
         name="customer-status"),

    path("Cooks/", CookListView.as_view(), name="cook-list"),
    path("Cooks/<int:pk>/", CookDetailView.as_view(), name="cook-details"),
    path("cook_status/<str:action>/<int:pk>/", cook_status, name="cook-status"),
    path("menu-catalog/<int:pk>", ViewCookMenuCatalog.as_view(), name="menu-catalog"),
    path("Cook-fsc/<int:pk>", ViewFSC.as_view(), name="FSC"),

    path('Couriers/', CourierListView.as_view(), name="courier-list"),
    path('Couriers/<int:pk>/', CourierDetailView.as_view(), name="courier-details"),
    path("view-courier/",
         TemplateView.as_view(template_name="dashboard/view-courier.html")),
    path("courier-order-details/<int:pk>",
         CourierOrderDetailView.as_view(), name="courier-order-details"),
    path("courier_status/<str:action>/<int:pk>/", courier_status,
         name="courier-status"),

    path("Orders/", OrderListView.as_view(), name="order-list"),
    path("Orders/<int:pk>/", OrderDetailsView.as_view(), name="order-details"),

    path("ReviewRating/", RatingListView.as_view(), name="review-rating"),
    path("ReviewRatingCook/", RatingListCookView.as_view(),
         name="review-rating-cook"),
    path("ReviewRatingCourier/", RatingListCourierView.as_view(),
         name="review-rating-courier"),
    path("StaticContent/", StaticContentView.as_view(), name="static-content"),
    path("StaticContent/TermCondition/<int:pk>/Edit/",
         TermAndConditionDetailView.as_view(), name="term-condition"),
    path("StaticContent/TermCondition/<int:pk>/Update/",
         TermAndConditionUpdateView.as_view(), name="term-condition-update"),
    path("StaticContent/PrivacyPolicy/<int:pk>/Edit/",
         PrivacyPolicyDetailView.as_view(), name="privacy-policy"),
    path("StaticContent/PrivacyPolicy/<int:pk>/Update/",
         PrivacyPolicyUpdateView.as_view(), name="privacy-policy-update"),

    path('Banners/', BannerListView.as_view(), name="banner-list"),
    path('Banners/Upload/', BannerCreateView.as_view(), name="banner-upload"),

    # path("notification-central/", TemplateView.as_view(template_name="dashboard/notification-central.html")),
    path('notification-central/', NotificationListView.as_view(),
         name="notification-central"),
    # path("all-apps-central-parameters/", TemplateView.as_view(template_name="dashboard/all-apps-central-parameters.html")),
    path('all-apps-central-parameters/', AllAppListView.as_view(),
         name="all-apps-central-parameters"),
    path("report-analysis/", ReportListView.as_view(), name="report-analysis"),
    path("operational-KPI/", OperationalKPIListView.as_view(),
         name="operational-KPI"),

    # APP CONFIG PARAMETERS
    path("app-configurations-parameters/", AppConfigListView.as_view(),
         name="app-configurations-parameters"),
    path("app-configurations-parameters-update/<int:id>/",
         AppConfigListViewUpdate.as_view(), name="app-configurations-parameters-update"),
    path("app-configurations-parameters-delete/<str:name>/<int:id>/",
         delete_item, name="app-configurations-parameters-delete"),

    path("communicate/", TemplateView.as_view(template_name="dashboard/communicate.html")),
    path("communicate/<int:pk>/",
         CommunicateDetailView.as_view(), name="communicate"),
    path("order-details/",
         TemplateView.as_view(template_name="dashboard/order-details.html")),


    # path("view-cook/", TemplateView.as_view(template_name="dashboard/view-cook.html")),
    path("view-cook/", TemplateView.as_view(template_name="dashboard/cook/cook_details.html")),
    path("food-safety-compliance/",
         TemplateView.as_view(template_name="dashboard/food-safety-compliance.html")),

    #path("view-cook-registration/", TemplateView.as_view(template_name="dashboard/view-cook-registration.html")),
    #path("view-cook-registration/<int:pk>/", ViewCookRegView.as_view(), name="cook-details-reg"),

    path("communicate-with-cook/",
         TemplateView.as_view(template_name="dashboard/communicate-with-cook.html")),
    path("fsc-details/", TemplateView.as_view(template_name="dashboard/fsc-details.html")),
    path("item-details/",
         TemplateView.as_view(template_name="dashboard/item-details.html")),
    path("view-fsc-result/", ViewCookFSCResult.as_view(), name="FSCResult"),
    #path("view-cook-cook-food-safety-compliance/", TemplateView.as_view(template_name="dashboard/view-cook-cook-food-safety-compliance.html")),
    path("view-cook-cook-food-safety-compliance/",
         ViewCookFSC.as_view(), name="ViewCookFSC"),

    path("view-cook-registration/", ViewCookRegView.as_view(), name='registration'),

    path("view-courier-communicate/",
         TemplateView.as_view(template_name="dashboard/view-courier-communicate.html")),
    #path("view-admin-validates-courier-information/", TemplateView.as_view(template_name="dashboard/view-admin-validates-courier-information.html")),

    path("view-admin-validates-courier-information/",
         ViewCourierInfo.as_view(), name="courier_info"),

    path("create-banner/",
         TemplateView.as_view(template_name="dashboard/create-banner.html")),

    path("order-managment-view/",
         TemplateView.as_view(template_name="dashboard/order-managment-view.html")),
    path("static-content-managment-edit/",
         TemplateView.as_view(template_name="dashboard/static-content-managment-edit.html")),
    path("edit-customer-support/",
         TemplateView.as_view(template_name="dashboard/edit-customer-support.html")),

    path("send_verification/", Send_Verification.as_view(),
         name="send_verification"),
    path("check_otp/", Check_OTP.as_view(), name="check_otp"),

    path("passwordcheck/", Change_Password.as_view(), name="passwordcheck"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
