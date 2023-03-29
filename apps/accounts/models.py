import jwt
import re
import datetime
import logging
import time
from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.contrib.postgres.fields import ArrayField

from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_otp.models import Device
from django_otp.oath import TOTP
from django_otp.util import hex_validator

from binascii import unhexlify
from apps.snippets.models import Country

from core import utils as base_utils
from core.constant import ACTIVE
from core.constant import STATUS_CHOICES
from core.models import TimestampedModel, Verification
from core.utils import default_key, upload_path_handler
# from core.otp import totp
from .querysets import UserQueryset
from .tasks import send_otp_on_mobile

SHA1_RE = re.compile('^[a-f0-9]{40}$')
token_generator = default_token_generator

logger = logging.getLogger("custom_logger")


#  Custom User Manager
class UserManager(BaseUserManager):

    def get_queryset(self):
        return UserQueryset(self.model, using=self._db)

    # Create User
    def _create_user(self, mobile_number, email, password, is_active=True, **extra_fields):

        if email is None:
            raise TypeError('User must have an email address.')

        email = self.normalize_email(email)
        user = self.model(mobile_number=mobile_number, email=email, **extra_fields)

        user.set_password(password)
        user.is_active = is_active
        user.save(using=self._db)
        return user

    # Create Normal User
    def create_user(self, mobile_number=None, email=None, password=None, is_active=True, send_sms=True, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        logger.info("creating user")
        user = self._create_user(mobile_number, email, password, is_active, **extra_fields)

        if send_sms:
            try:
                logger.info("sending email")
                user.send_activation_email()
            except Exception as e:
                logger.info("email error", e)

        return user

    # Create Super User
    def create_superuser(self, mobile_number, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('has_email_verified', True)
        extra_fields.setdefault('has_mobile_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile_number, email, password, is_active=True, **extra_fields)

    # Activate User
    def activate_user_mobile(self, user):
        user.is_active = True
        user.has_mobile_verified = True
        user.save()
        return user

    # Check Token Expired or Not
    def expired(self):

        now = timezone.now() if settings.USE_TZ else datetime.datetime.now()

        return self.exclude(
            models.Q(user__is_active=True) |
            models.Q(verification_key=User.ACTIVATED)
        ).filter(
            user__date_joined__lt=now - datetime.timedelta(
                getattr(settings, 'VERIFICATION_KEY_EXPIRY_DAYS', 4)
            )
        )


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin, TimestampedModel, Verification):
    ACTIVATED = "ALREADY ACTIVATED"

    CUSTOMER = 'customer'
    COURIER = 'courier'
    COOK = 'cook'

    ROLE_CHOICES = (
        (CUSTOMER, 'Customer'),
        (COURIER, 'Courier'),
        (COOK, 'Cook')
    )

    user_id = models.BigAutoField(primary_key=True, editable=False)
    username = models.CharField(max_length=50, blank=True)
    email = models.EmailField(db_index=True, unique=True)
    isd_code = models.CharField(
        max_length=20,
        help_text=_('Country ISD Code')
    )
    mobile_number = models.CharField(
        max_length=16,
        db_index=True,
        unique=True
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    role = ArrayField(
        models.CharField(
            max_length=12,
            choices=ROLE_CHOICES
        ),
        default=list,
        blank=True
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number', ]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.slug = self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    # META CLASS
    class Meta:
        db_table = 'table_user_account'
        verbose_name = 'user'
        verbose_name_plural = 'User Management'

    def __str__(self):
        return f"{self.email} - {self.mobile_number}"

    @property
    def otp(self):
        return self.verification_key

    @property
    def last_role(self):
        if not self.role:
            return None
        return self.role[-1]

    # Generate Verification Key
    def verification_key_expired(self):
        expiration_date = timedelta(
            days=getattr(settings, 'VERIFICATION_KEY_EXPIRY_DAYS', 4)
        )

        return self.verification_key == self.ACTIVATED or True

    # Send Email Verification Mail
    def send_activation_email(self):

        context = {
            'verification_key': self.verification_key,
            'user': self,
        }
        logger.info('context created')
        subject = render_to_string(
            'registration/activation_email_subject.txt', context
        )
        logger.info('subject created')
        subject = ''.join(subject.splitlines())

        message = render_to_string(
            'registration/activation_email_content.txt', context
        )
        logger.info('message created')
        msg = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.attach_alternative(message, "text/html")
        logger.info('Alternative attached')
        msg.send()
        logger.info('Email Sent')

    # Send Password Reset EMail
    def send_password_reset_email(self, site, otp):

        context = {
            'email': self.email,
            'uid': base_utils.base36encode(self.pk),
            'user': self,
            'otp': otp
        }
        subject = render_to_string(
            'password_reset/password_reset_email_subject.txt', context
        )

        subject = ''.join(subject.splitlines())

        message = render_to_string(
            'password_reset/password_reset_email_content.txt', context
        )

        msg = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.attach_alternative(message, "text/html")
        # msg.send(fail_silently=True)

    @property
    def is_cook(self):
        return self.COOK in self.role

    @property
    def is_courier(self):
        return self.COURIER in self.role

    @property
    def is_customer(self):
        return self.CUSTOMER in self.role

    def token(self, role):
        return self._generate_jwt_token(role)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self, role):

        dt = datetime.now() + timedelta(days=7)

        token = jwt.encode({
            'id': self.pk,
            'role': role,
            # 'exp': int(dt.strftime('%s'))
            'exp': dt
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class StoreToken(TimestampedModel):

    ANDROID = '0'
    IOS = '1'
    Windows = '2'
    MacOS = '3'

    DEVICE_CHOICES = (
        (ANDROID, 'Android'),
        (IOS, 'iOS'),
        (Windows, 'Windows'),
        (MacOS, 'MacOS')
    )

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    device_type = models.CharField(choices=DEVICE_CHOICES, max_length=255, null=True, blank=True)
    device_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user_id}"

    class Meta:
        db_table = 'table_store_token'


class StripeCustomerUser(TimestampedModel):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user_id}"

    class Meta:
        db_table = 'table_stripe_customer_user'


class BankAccount(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    account_no = models.CharField(max_length=30, null=True, blank=True)
    account_holder_name = models.CharField(max_length=255, null=True, blank=True)
    bank_ifsc_code = models.CharField(max_length=20, null=True, blank=True)


"""
class VerificationDevice(Device):
    mobile_number = models.CharField(max_length=16, unique=True)
    secret_key = models.CharField(
        max_length=40,
        default=default_key,
        validators=[hex_validator],
        help_text="Hex-encoded secret key to generate totp tokens.",
        unique=True,
    )
    last_verified_counter = models.BigIntegerField(
        default=-1,
        help_text=("The counter value of the latest verified token."
                   "The next token must be at a higher counter value."
                   "It makes sure a token is used only once.")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='devices')
    verified = models.BooleanField(default=False)
    otp = models.IntegerField(null=True, blank=True)

    step = settings.TOTP_TOKEN_VALIDITY
    digits = settings.TOTP_DIGITS

    class Meta(Device.Meta):
        verbose_name = "Verification Device"

    @property
    def bin_key(self):
        return unhexlify(self.secret_key.encode())

    def totp_obj(self):
        totp = TOTP(key=self.bin_key, step=self.step, digits=self.digits)
        totp.time = time.time()
        return totp

    def generate_challenge(self):
        totp = self.totp_obj()
        token = str(totp.token()).zfill(self.digits)

        message = _("Your token for Cangurhu is {token_value}."
                    " It is valid for {time_validity} minutes.")
        message = message.format(token_value=token, time_validity=self.step // 60)

        logger.debug("Token has been sent to %s " % self.mobile_number)
        logger.debug("%s" % message)

        return token

    def verify_token(self, token: int, tolerance: int = 0):
        totp = self.totp_obj()
        if ((totp.t() > self.last_verified_counter) and
                (totp.verify(token, tolerance=tolerance))):
            self.last_verified_counter = totp.t()
            self.verified = True
            self.save()
        else:
            self.verified = False
        return self.verified
"""
