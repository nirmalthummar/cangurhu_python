import secrets
from abc import ABC

from django.core.cache import cache
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework import status
from core.otp import TOTPVerification  # totp
from core.exceptions import UnauthorizedException

from apps.accounts.models import StoreToken, StripeCustomerUser, BankAccount
from twilio.rest import Client
from cangurhu.settings import ACCOUNT_SID, AUTH_TOKEN, PHONE_NUMBER

from apps.snippets.models import Country
from apps.snippets.api.serializers import CountrySerializer

User = get_user_model()

ANDROID = 0
IOS = 1
Windows = 2
MacOS = 3

DEVICE_CHOICES = (
    (ANDROID, 'Android'),
    (IOS, 'iOS'),
    (Windows, 'Windows'),
    (MacOS, 'MacOS')
)

LOGIN = 'LOGIN'
SIGNUP = 'SIGNUP'
FORGOT_PASSWORD = 'FORGOT_PASSWORD'

OTP_TYPE_CHOICES = (
    (LOGIN, 'Login'),
    (SIGNUP, 'Signup'),
    (FORGOT_PASSWORD, 'Forgot Password')
)

client = Client(ACCOUNT_SID, AUTH_TOKEN)
sender_contact_number = PHONE_NUMBER


def send_sms(client, body, sender_contact_number, customer_contact_number):
    message = client.messages.create(
        body=body,
        from_=sender_contact_number,
        to=customer_contact_number
    )
    return message


class RegistrationSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True, write_only=True)
    device_type = serializers.CharField(max_length=255, required=True, write_only=True)
    device_token = serializers.CharField(max_length=255, required=True, write_only=True)
    otp = serializers.SerializerMethodField(read_only=True)

    # device_type_new = serializers.SerializerMethodField(required=True, write_only=True)
    # device_token_new = serializers.SerializerMethodField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'email', 'username', 'isd_code', 'mobile_number',
                  'role', 'device_type', 'device_token', 'otp')

        extra_kwargs = {
            "username": {"required": True}
        }

    def get_otp(self, obj):
        signup_cache_key = f"{obj.role[-1]}~{SIGNUP}~{obj.mobile_number}".upper()
        if not signup_cache_key:
            return None
        return str(cache.get(signup_cache_key))

    def create(self, validated_data):
        device_type = validated_data.pop('device_type')
        device_token = validated_data.pop('device_token')
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data, password=secrets.token_hex(16))
        user.role.append(role)
        user.save()

        try:
            store_token = StoreToken.objects.get(user_id=user, device_type=device_type)
            store_token.device_token = device_token
            store_token.save()

        except StoreToken.DoesNotExist:
            store_token = StoreToken.objects.create(
                user_id=user,
                device_type=device_type,
                device_token=device_token
            )

        totp = TOTPVerification()
        otp_token = totp.generate_token()
        signup_cache_key = f"{role}~{SIGNUP}~{user.mobile_number}".upper()
        cache.set(signup_cache_key, otp_token, timeout=300)
        try:
            body = f"Dear User, Your One Time Password is - {otp_token}"
            message = send_sms(client, body, sender_contact_number, user.mobile_number)
            print(user.mobile_number)
            print(message)
        except Exception as e:
            print(e)
        return user


# User Login Serializer
class LoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=16, required=True)
    otp = serializers.CharField(max_length=4, read_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
    device_type = serializers.CharField(max_length=255, required=True)
    device_token = serializers.CharField(max_length=255, required=True)

    def authenticate(self, mobile_number=None):
        try:
            user = User.objects.get(mobile_number=mobile_number)
        except User.DoesNotExist:
            return None
        return user

    def validate(self, data):
        mobile_number = data.get('mobile_number', None)
        role = data.get('role', None)

        if mobile_number is None:
            raise serializers.ValidationError(
                'A mobile number is required to log in.'
            )

        if role is None:
            raise serializers.ValidationError(
                'A user role is required to log in.'
            )

        user = self.authenticate(mobile_number=mobile_number)

        if user is None:
            raise serializers.ValidationError(
                'A user with this mobile number was not found.'
            )

        if role not in user.role:
            raise serializers.ValidationError(
                'This user role does not match.'
            )

        if not user.has_mobile_verified:
            raise UnauthorizedException(
                detail='Mobile number is not verified.',
                field='mobile_number',
                status_code=440
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        totp = TOTPVerification()
        otp_token = totp.generate_token()
        login_cache_key = f"{role}~{LOGIN}~{mobile_number}".upper()
        cache.set(login_cache_key, otp_token, timeout=180)

        device_type = data.get('device_type', None)
        device_token = data.get('device_token', None)

        try:
            store_token = StoreToken.objects.get(user_id=user, device_type=device_type)
            store_token.device_token = device_token
            store_token.save()

        except StoreToken.DoesNotExist:
            store_token = StoreToken.objects.create(
                user_id=user,
                device_type=device_type,
                device_token=device_token
            )
        try:
            body = f"Dear User, Your One Time Password is - {otp_token}"
            message = send_sms(client, body, sender_contact_number, user.mobile_number)
            print(message)
        except Exception as e:
            print(e)
        return {
            'role': role,
            'mobile_number': user.mobile_number,
            "otp": otp_token,
            'device_type': store_token.device_type,
            'device_token': store_token.device_token
        }


# OTP Verification
class OTPVerifySerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=16, required=True)
    otp = serializers.CharField(required=True, write_only=True)
    otp_type = serializers.ChoiceField(choices=OTP_TYPE_CHOICES, required=True, write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    email = serializers.CharField(max_length=255, read_only=True)
    isd_code = serializers.CharField(max_length=16, read_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    has_mobile_verified = serializers.BooleanField(read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        mobile_number = data.get('mobile_number')
        otp = data.get('otp')
        otp_type = data.get('otp_type')
        role = data.get('role')

        try:
            user = User.objects.get(mobile_number=mobile_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("Mobile number does not exists!!")

        otp_cache_key = f"{role}~{otp_type}~{mobile_number}".upper()
        otp_token = cache.get(otp_cache_key)

        if not otp_token:
            raise serializers.ValidationError("Invalid OTP 1")

        if otp != str(otp_token):
            raise serializers.ValidationError("Invalid OTP 2")

        # totp = TOTPVerification()
        # verified = totp.verify_token(int(otp))
        # print(verified)
        # if not verified:
        #     raise serializers.ValidationError("Invalid OTP 3")

        if otp_type == SIGNUP:
            activated_user = User.objects.activate_user_mobile(user)

        return {
            'user_id': user.pk,
            'email': user.email,
            'role': role,
            'isd_code': user.isd_code,
            'mobile_number': user.mobile_number,
            'username': user.username,
            'has_mobile_verified': user.has_mobile_verified,
            'token': user.token(role)
        }


# Resend OTP
class ResendOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=True)
    message = serializers.CharField(read_only=True)
    otp = serializers.CharField(read_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    otp_type = serializers.ChoiceField(choices=OTP_TYPE_CHOICES, required=True, write_only=True)

    def validate(self, data):
        mobile_number = data.get('mobile_number')
        role = data.get('role')

        try:
            user = User.objects.get(mobile_number=mobile_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("Mobile number does not exists!!")

        totp = TOTPVerification()
        otp_token = totp.generate_token()
        login_cache_key = f"{role}~{LOGIN}~{mobile_number}".upper()
        cache.set(login_cache_key, otp_token, timeout=180)
        try:
            body = f"Dear User, Your One Time Password is - {otp_token}"
            message = send_sms(client, body, sender_contact_number, mobile_number)
            print(message)
        except Exception as e:
            print(e)
        return {
            "message": "OTP has been sent to %s " % mobile_number,
            "otp": otp_token,
            "role": role,
            "mobile_number": mobile_number
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, required=True, allow_blank=True)
    mobile_number = serializers.CharField(max_length=16, required=False, allow_blank=True)
    isd_code = serializers.CharField(max_length=10, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', 'password', 'mobile_number', 'isd_code', 'role')


class GenerateTokenSerializer(serializers.Serializer):
    customer = serializers.CharField(max_length=255)
    cook = serializers.CharField(max_length=255)
    courier = serializers.CharField(max_length=255)


class SendOtpSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    message = serializers.CharField(read_only=True)
    otp = serializers.CharField(read_only=True)

    def validate(self, data):
        mobile_number = data.get('mobile_number')
        email = data.get('email')
        totp = TOTPVerification()
        otp_token = totp.generate_token()
        if mobile_number:
            cache_key = f"{mobile_number}".upper()
            cache.set(cache_key, otp_token, timeout=180)
            try:
                body = f"Dear User, Your One Time Password is - {otp_token}"
                message = send_sms(client, body, sender_contact_number, mobile_number)
                print(message)
            except Exception as e:
                print(e)
        if email:
            cache_key = f"{email}"
            cache.set(cache_key, otp_token, timeout=180)

        return {
            "message": "OTP has been sent",
            "otp": otp_token,
            "mobile_number": mobile_number,
            "email": email
        }


class VerifyOtpSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=16, required=False)
    email = serializers.CharField(max_length=25, required=False)
    message = serializers.CharField(read_only=True)
    otp = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        mobile_number = data.get('mobile_number')
        email = data.get('email')
        otp = data.get('otp')

        if mobile_number:
            verify_cache = cache.get(mobile_number)

            if verify_cache == otp:
                user_id = self.context.get("user_id")
                user = User.objects.get(user_id=user_id)
                user.mobile_number = mobile_number
                user.save()
                return {
                    "message": "Mobile number successfully updated",
                }
            else:
                raise serializers.ValidationError("Invalid OTP")

        if email:
            verify_cache = cache.get(email)

            if verify_cache == otp:
                user_id = self.context.get("user_id")
                user = User.objects.get(user_id=user_id)
                user.email = email
                user.save()
                return {
                    "message": "Email successfully updated",
                }

            else:
                raise serializers.ValidationError("Invalid OTP")


class StripeCustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeCustomerUser
        fields = "__all__"


class BankAccountSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    class Meta:
        model = BankAccount
        fields = ['id', 'user', 'country', 'bank_name', 'account_no', 'account_holder_name', 'bank_ifsc_code']

    def validate(self, data):
        acc = data.get("account_no")
        ifsc = data.get("bank_ifsc_code")

        if len(acc) != 11:
            raise serializers.ValidationError({"account_no": "Invalid Format. Only 11 Digits are allowed."})
        if len(ifsc) != 11:
            raise serializers.ValidationError({"bank_ifsc_code": "Invalid Format. Only 11 Digits are allowed."})
        return data

    @staticmethod
    def get_user(obj):
        return UserSerializer(obj.user).data

    @staticmethod
    def get_country(obj):
        return CountrySerializer(obj.country).data
