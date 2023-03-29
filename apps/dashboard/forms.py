from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Please enter a correct email and password."
        ),
        'inactive': _("This account is inactive."),
        'not_verified': _("Email not verified")
    }
    username = forms.EmailField(required=True)

    def authenticate(self, request=None, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and getattr(user, 'is_superuser', False) and user.check_password(password):
                return user
        return None

    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = self.authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

        if not user.is_superuser:
            raise ValidationError(
                self.error_messages['inactive'],
                code='invalid_login',
            )

        if not user.has_email_verified:
            raise ValidationError(
                self.error_messages['not_verified'],
                code='inactive',
            )


class ForgetPasswordForm(forms.Form):
    error_messages = {
        'required': _('Email is required field!'),
    }
    email = forms.EmailField(
        max_length=254,
        required=True
    )

    def get_user(self, email=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and getattr(user, 'is_superuser', False):
                return user
        return None

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = self.get_user(email)
        if not user:
            self.add_error("email", _("A user with this email does not exists."))
        return email


class ResetPasswordForm(SetPasswordForm):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'required': _('Password and Confirm are required are required!.'),
        'password_mismatch': _('Password and Confirm password didn’t match.'),
    }

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        # password_validation.validate_password(password2, self.user)
        return password2
