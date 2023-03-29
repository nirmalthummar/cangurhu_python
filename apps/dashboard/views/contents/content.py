from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.contents.models import TermAndCondition, PrivacyPolicy
from core.constant import ACTIVE


class StaticContentView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/contents/static_content.html"

    def get_term_condition(self):
        return TermAndCondition.objects.filter(status=ACTIVE).last()

    def get_privacy_policy(self):
        return PrivacyPolicy.objects.filter(status=ACTIVE).last()

    def get_context_data(self, **kwargs):
        context = super(StaticContentView, self).get_context_data(**kwargs)
        context['content_active'] = True
        context['term_active'] = True
        context['term'] = self.get_term_condition()
        context['policy'] = self.get_privacy_policy()
        print(context)
        return context
