from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.constant import ACTIVE
from apps.contents.models import (
    TermAndCondition,
    PrivacyPolicy,
    Faqs, LandingPageContent
)
from apps.contents.api.serializers import (
    TermAndConditionSerializer,
    PrivacyPolicySerializer,
    FaqsSerializer, LandingPageContentSerializer
)


class TermAndConditionAPIView(APIView):
    serializer_class = TermAndConditionSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return TermAndCondition.objects.filter(status=ACTIVE).last()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PrivacyPolicyAPIView(APIView):
    serializer_class = PrivacyPolicySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return PrivacyPolicy.objects.filter(status=ACTIVE).last()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FaqsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
            Get all the Faqs
        """

        queryset = Faqs.objects.filter(active=True)

        serializer = FaqsSerializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class LandingPageContentAPIView(APIView):
    serializer_class = LandingPageContentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return LandingPageContent.objects.filter(status=ACTIVE).last()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
