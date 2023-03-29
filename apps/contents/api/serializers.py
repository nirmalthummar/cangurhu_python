from rest_framework import serializers

from apps.contents.models import (
    TermAndCondition,
    PrivacyPolicy,
    Faqs,
    LandingPageContent,
)


class TermAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermAndCondition
        fields = ('term_heading_text', 'term_body_text')


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ('policy_heading_text', 'policy_body_text')


class FaqsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faqs
        fields = "__all__"


class LandingPageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPageContent
        fields = "__all__"
