from django import forms
from django_summernote.fields import SummernoteTextField
from .models import TermAndCondition, PrivacyPolicy


class TermAndConditionForm(forms.ModelForm):
    term_body_text = SummernoteTextField()

    class Meta:
        model = TermAndCondition
        fields = ('term_heading_text', 'term_body_text')


class PrivacyPolicyForm(forms.ModelForm):
    policy_body_text = SummernoteTextField()

    class Meta:
        model = PrivacyPolicy
        fields = ('policy_heading_text', 'policy_body_text')

