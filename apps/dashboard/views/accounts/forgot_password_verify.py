from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from django.utils.http import is_safe_url
from django.contrib import messages


class ForgotPasswordVerifyView(View):
    def authenticate(self, email=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and getattr(user, 'is_superuser', False):
                return user
        return None

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user = self.authenticate(email=email)

        if not user:
            messages.error(request, "Email not found in our record!!")

        if user is not None:
            next_url = request.GET.get('next', None)
            if user.is_active:
                login(request, user)
                if next_url is not None and is_safe_url(next_url, settings.ALLOWED_HOSTS):
                    return redirect(next_url)
                return redirect(reverse('dashboard:home'))
            else:
                messages.error(request, 'Account is deactivated, you can not reset the password.')
        return HttpResponseRedirect(settings.LOGIN_URL)
