from django.contrib import admin

# Register your models here.
from django_summernote.admin import SummernoteModelAdmin
from apps.contents.models import TermAndCondition, PrivacyPolicy, Banner, Faqs, TranslatedUser, TranslateData, \
    LandingPageContent


class TermAndConditionAdmin(SummernoteModelAdmin):
    summernote_fields = ('term_body_text',)


class PrivacyPolicyAdmin(SummernoteModelAdmin):
    summernote_fields = ('policy_body_text',)


admin.site.register(TermAndCondition, TermAndConditionAdmin)
admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)
admin.site.register(Banner)
admin.site.register(TranslateData)
admin.site.register(TranslatedUser)


class FaqsAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'active')


class LandingPageContentAdmin(admin.ModelAdmin):
    list_display = (
        'cook_heading', 'cook_body', 'courier_heading', 'courier_body', 'customer_heading', 'customer_body')


admin.site.register(LandingPageContent, LandingPageContentAdmin)
admin.site.register(Faqs, FaqsAdmin)
