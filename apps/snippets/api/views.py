from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.snippets.models import Country
from .serializers import CountrySerializer


class CountryListAPIView(generics.ListAPIView):
    """
    Return country list
    """
    permission_classes = (AllowAny,)
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    swagger_tags = ['Snippets']