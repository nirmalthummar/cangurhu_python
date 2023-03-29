from django.urls import path
from apps.rating.api.views import CookFeedbackView, CookFeedbackDetailView

app_name = 'rating'

urlpatterns = [
    path('feedback-rating', CookFeedbackView.as_view(), name='cook-feedback'),
    path('feedback-rating/<int:feedback_id>', CookFeedbackDetailView.as_view(), name='cook-feedback-detail'),
]
