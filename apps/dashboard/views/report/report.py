from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic import TemplateView


class ReportListView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/report-analysis.html"

    def get_context_data(self, **kwargs):
        context = super(ReportListView, self).get_context_data(**kwargs)
        context['report_active'] = True
        return context
