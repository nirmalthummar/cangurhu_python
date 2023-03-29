from django.urls import path
from .views import (
    TermAndConditionAPIView,
    PrivacyPolicyAPIView,
    FaqsView, LandingPageContentAPIView
)

app_name = 'contents'
urlpatterns = [
    path('term-condition/', TermAndConditionAPIView.as_view(), name='term_condition'),
    path('privacy-policy/', PrivacyPolicyAPIView.as_view(), name='privacy_policy'),
    path('faqs/', FaqsView.as_view(), name='faqs'),
    path('landing-page-content/', LandingPageContentAPIView.as_view(), name='landing_page_content'),
]