from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from apps.contents.models import Banner
from core.constant import ACTIVE


class BannerListView(LoginRequiredMixin, ListView):
    model = Banner
    template_name = "dashboard/contents/banner_list.html"
    context_object_name = "object_list"
    queryset = Banner.objects.filter(status=ACTIVE)

    def get_context_data(self, **kwargs):
        context = super(BannerListView, self).get_context_data(**kwargs)
        context['banner_active'] = True
        return context


class BannerCreateView(CreateView):
    template_name = "dashboard/contents/banner_upload.html"
    model = Banner
    fields = ['banner_image', 'send_to_all', ]

    def get_context_data(self, **kwargs):
        context = super(BannerCreateView, self).get_context_data(**kwargs)
        context['banner_active'] = True
        return context