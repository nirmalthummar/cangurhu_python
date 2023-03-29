from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from apps.contents.models import PrivacyPolicy
from apps.contents.forms import PrivacyPolicyForm
from core.constant import ACTIVE


class PrivacyPolicyDetailView(LoginRequiredMixin, DetailView):
    model = PrivacyPolicy
    template_name = "dashboard/contents/privacy_policy_edit.html"
    queryset = PrivacyPolicy.objects.filter(status=ACTIVE)
    context_object_name = "policy"
    form_class = PrivacyPolicyForm

    def get_context_data(self, **kwargs):
        context = super(PrivacyPolicyDetailView, self).get_context_data(**kwargs)
        context['content_active'] = True
        context['policy_active'] = True
        context['form'] = self.form_class(instance=self.get_object())
        return context


class PrivacyPolicyUpdateView(LoginRequiredMixin, UpdateView):
    model = PrivacyPolicy
    template_name = "dashboard/contents/privacy_policy_edit.html"
    queryset = PrivacyPolicy.objects.filter(status=ACTIVE)
    context_object_name = "policy"
    fields = ['policy_body_text', ]

    def get_context_data(self, **kwargs):
        context = super(PrivacyPolicyUpdateView, self).get_context_data(**kwargs)
        context['content_active'] = True
        context['policy_active'] = True
        return context
