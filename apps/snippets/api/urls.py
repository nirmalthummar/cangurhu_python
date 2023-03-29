from django.urls import path
from .views import (
    CountryListAPIView
)

app_name = 'snippets'
urlpatterns = [
    path('country/', CountryListAPIView.as_view(), name='country'),
]