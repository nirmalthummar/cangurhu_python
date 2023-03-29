from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from django.contrib import messages
from apps.dashboard.forms import ForgetPasswordForm
from core.otp import TOTPVerification


class ForgotPasswordView(View):
    template_name = "dashboard/accounts/forgot_password.html"
    otp_template_name = "dashboard/accounts/forgot_password_verify.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard:home'))

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = form.get_user(email)
            if user:
                totp = TOTPVerification()
                generated_token = totp.generate_token()
                cache.set("email", generated_token, timeout=300)
                user.send_password_reset_email(site=get_current_site(request), otp=generated_token)
            messages.success(request, "Password reset link has been sent to your linked email.")
            return render(request, self.otp_template_name)

        error_msg = "A user with this email does not exists."
        form_error = list(form.error_messages.values())
        if form_error:
            error_msg = form_error[0]
        messages.error(request, error_msg)
        return render(request, self.template_name, {'form': form})
