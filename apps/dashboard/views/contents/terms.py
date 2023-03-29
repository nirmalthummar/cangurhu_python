from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.views.generic.edit import FormMixin
from apps.contents.models import TermAndCondition
from apps.contents.forms import TermAndConditionForm
from core.constant import ACTIVE


class TermAndConditionDetailView(LoginRequiredMixin, DetailView):
    model = TermAndCondition
    template_name = "dashboard/contents/term_condition_edit.html"
    queryset = TermAndCondition.objects.filter(status=ACTIVE)
    context_object_name = "term"
    form_class = TermAndConditionForm

    def get_context_data(self, **kwargs):
        context = super(TermAndConditionDetailView, self).get_context_data(**kwargs)
        context['content_active'] = True
        context['term_active'] = True
        context['form'] = self.form_class(instance=self.get_object())
        return context


class TermAndConditionUpdateView(LoginRequiredMixin, UpdateView):
    model = TermAndCondition
    template_name = "dashboard/contents/term_condition_edit.html"
    queryset = TermAndCondition.objects.filter(status=ACTIVE)
    context_object_name = "term"
    fields = ['term_body_text', ]

    def get_context_data(self, **kwargs):
        context = super(TermAndConditionUpdateView, self).get_context_data(**kwargs)
        context['content_active'] = True
        context['term_active'] = True
        return context
