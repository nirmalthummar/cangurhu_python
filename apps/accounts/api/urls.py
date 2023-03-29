from django.urls import path, include
from rest_auth.registration.views import SocialLoginView

from apps.accounts.api.views import (
    BankAccountDetailsView,
    BankAccountDetailsEditView,
    LoginAPIView,
    RegistrationAPIView,
    UserMobileVerificationAPIView,
    ResendOTPAPIView,
    UserRetrieveUpdateAPIView,
    GenerateToken,
    SendOtpView,
    UpdateUserCredentials,
    StripeCustomerUserView
)

app_name = 'accounts'
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='user'),
    path('users/', RegistrationAPIView.as_view(), name='signup'),
    path('users/login/', LoginAPIView.as_view(), name='login'),

    path('mobile/verify/', UserMobileVerificationAPIView.as_view(), name='mobile_verify'),
    path('mobile/resend-otp/', ResendOTPAPIView.as_view(), name='mobile_resend_otp'),
    path('generate-token/', GenerateToken.as_view(), name="generate-token"),

    # to update user email/mobile_number

    path('mobile/send-otp/', SendOtpView.as_view(), name='send_otp'),
    path('mobile/update/', UpdateUserCredentials.as_view(), name='update_number'),

    path('users/stripe-user/', StripeCustomerUserView.as_view(), name='stripe-customer-user'),
    
    path('users/bank-account-details/', BankAccountDetailsView.as_view(), name='user-bank-account'),
    path('users/bank-account-details/edit/<int:pk>/', BankAccountDetailsEditView.as_view(), name='edit-user-bank-account'),

    # all-auth
    path('rest-auth/facebook/', SocialLoginView.as_view()),
    path('rest-auth/google/', SocialLoginView.as_view()),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),


]
