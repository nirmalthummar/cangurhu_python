from email import message
from os import stat
from urllib import response
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from requests import delete
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from uritemplate import partial
from common.exception import ErrorResponseException

from core.permissions import IsCustomer
from apps.accounts.models import StripeCustomerUser

from core.permissions import IsOwnerOrReadOnly
from core.permissions import IsCourier, IsCook
from apps.accounts.models import BankAccount
from .serializers import (
    BankAccountSerializer,
    LoginSerializer,
    RegistrationSerializer,
    OTPVerifySerializer,
    ResendOTPSerializer,
    UserSerializer,
    GenerateTokenSerializer,
    SendOtpSerializer,
    VerifyOtpSerializer,
    StripeCustomerUserSerializer
)

User = get_user_model()

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class RegistrationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    swagger_tags = ['Accounts']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        extra_data = {
            'role': request.data.get('role', ''),
            'device_type': request.data.get('device_type', ''),
            'device_token': request.data.get('device_token', '')
        }

        extra_data.update(serializer.data)

        return Response(extra_data, status=status.HTTP_201_CREATED)


# Login View
class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    swagger_tags = ['Accounts']

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: LoginSerializer(),
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserMobileVerificationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OTPVerifySerializer
    swagger_tags = ['Accounts']

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: OTPVerifySerializer(),
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResendOTPAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResendOTPSerializer
    swagger_tags = ['Accounts']

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ResendOTPSerializer(),
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    swagger_tags = ['Accounts']

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenerateToken(GenericAPIView):
    swagger_tags = ['Others']
    serializer_class = GenerateTokenSerializer

    def get(self, request):
        number = request.query_params.get('number', '9898989899')
        print("number", number)
        user = User.objects.filter(mobile_number=number).first()
        print("user", user)
        customer = user.token(User.CUSTOMER)
        courier = user.token(User.COURIER)
        cook = user.token(User.COOK)

        token = {
            "customer": customer,
            "cook": cook,
            "courier": courier
        }
        serializer = self.get_serializer(token)
        return Response(serializer.data)


class SendOtpView(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = SendOtpSerializer
    swagger_tags = ['Send otp']

    """
    send otp for mobile and email update
    
    """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: SendOtpSerializer(),
        }
    )
    def post(self, request):
        serializer = SendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserCredentials(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = VerifyOtpSerializer
    swagger_tags = ['Update Mobile Number and Email']

    """
    verify otp and update mobile number and email by sending otp
    
    """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: VerifyOtpSerializer(),
        }
    )
    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data, context={"user_id": request.user.user_id})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StripeCustomerUserView(APIView):
    permission_classes = (IsCustomer,)

    def get(self, request):
        """
            Get stripe customer id
        """
        user_id = request.user.user_id

        try:
            stripe_customer = StripeCustomerUser.objects.get(user_id=user_id)

        except StripeCustomerUser.DoesNotExist:
            raise ErrorResponseException(f"Stripe customer is not exist!")

        serializer = StripeCustomerUserSerializer(stripe_customer)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """
            Store Stripe customer id
        """
        user_id = request.user.user_id

        payload = request.data

        try:
            stripe_customer = StripeCustomerUser.objects.get(user_id=user_id)

        except StripeCustomerUser.DoesNotExist:
            stripe_customer_id = payload.get('stripe_customer_id')
            if not stripe_customer_id:
                raise ErrorResponseException("'stripe_customer_id' is missing!")

            payload['user_id'] = user_id

            serializer = StripeCustomerUserSerializer(data=payload)

            if serializer.is_valid():
                serializer.save()

            else:
                raise ErrorResponseException(serializer.errors)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        if stripe_customer:
            raise ErrorResponseException(f"Stripe customer id is already exist with customer {request.user.username}")


class BankAccountDetailsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        try:
            user_bank_details = BankAccount.objects.filter(user=user)
        except BankAccount.DoesNotExist:
            raise ErrorResponseException("No bank account details found.")

        serializer = BankAccountSerializer(user_bank_details, many=True)
        return Response(serializer.data)

    def post(self, request):
        role = request.user.role[0]
        if role == "customer":
            country = request.user.customer.country
        elif role == "cook":
            country = request.user.cook.country
        elif role == "courier":
            country = request.user.courier.country

        serializer = BankAccountSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user, country=country)
            return Response(serializer.data)
        else:
            raise ErrorResponseException(str(serializer.errors))


class BankAccountDetailsEditView(APIView):
    def get(self, request, pk):
        try:
            user_bank_details = BankAccount.objects.get(id=pk)
        except BankAccount.DoesNotExist:
            raise ErrorResponseException("No bank account details found.")

        serializer = BankAccountSerializer(user_bank_details)
        return Response(serializer.data)

    def put(self, request, pk):
        bank_detail = BankAccount.objects.get(id=pk)

        payload = request.data

        bank_name = payload.get('bank_name')
        if not bank_name:
            raise ErrorResponseException("Please enter bank name.")

        account_no = payload.get('account_no')
        if not account_no:
            raise ErrorResponseException("Please provide account number.")

        account_holder_name = payload.get('account_holder_name')
        if not account_holder_name:
            raise ErrorResponseException("Please enter account holder's name.")

        bank_ifsc_code = payload.get('bank_ifsc_code')
        if not bank_ifsc_code:
            raise ErrorResponseException("Please enter Bank IFSC code.")

        serializer = BankAccountSerializer(data=payload, instance=bank_detail)
        if serializer.is_valid():
            try:
                bank_detail.bank_name = payload.get("bank_name")
                bank_detail.account_no = payload.get("account_no")
                bank_detail.account_holder_name = payload.get("account_holder_name")
                bank_detail.bank_ifsc_code = payload.get("bank_ifsc_code")
                bank_detail.save()
            except Exception as e:
                raise ErrorResponseException(e)
            serializer.save()
        else:
            raise ErrorResponseException(str(serializer.errors))

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        bank_detail = BankAccount.objects.get(id=pk)
        message = f"Bank account details for user ({bank_detail.user.username}) have been deleted successfully."
        bank_detail.delete()
        return Response(message)
