from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic import TemplateView


class RatingListView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/review_rating_management_dish.html"

    def get_context_data(self, **kwargs):
        context = super(RatingListView, self).get_context_data(**kwargs)
        context['rating_active'] = True
        return context


class RatingListCookView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/review-rating-management_cook.html"

    def get_context_data(self, **kwargs):
        context = super(RatingListCookView, self).get_context_data(**kwargs)
        context['rating_active'] = True
        return context

class RatingListCourierView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/review-rating-management_courier.html"

    def get_context_data(self, **kwargs):
        context = super(RatingListCourierView, self).get_context_data(**kwargs)
        context['rating_active'] = True
        return context