from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.snippets.models import Country
from core.models import TimestampedModel
from core.constant import ACTIVE
from core.constant import STATUS_CHOICES


class TermAndCondition(TimestampedModel):
    term_condition_id = models.BigAutoField(primary_key=True, editable=False)
    term_heading_text = models.CharField(
        _("Term body text in english."),
        max_length=255,
        null=True,
        blank=True
    )
    term_body_text = models.TextField(
        _("Term body text in english."),
        null=True,
        blank=True
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        db_table = "table_term_condition"
        verbose_name = "Term & Condition"
        verbose_name_plural = "Terms & Conditions"

    def __str__(self):
        if self.term_heading_text:
            return self.term_heading_text
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('dashboard:term-condition', args=[str(self.pk)])


class PrivacyPolicy(TimestampedModel):
    privacy_policy_id = models.BigAutoField(primary_key=True, editable=False)
    policy_heading_text = models.CharField(
        _("Term body text in english."),
        max_length=255,
        null=True,
        blank=True
    )
    policy_body_text = models.TextField(
        _("Term body text in english."),
        null=True,
        blank=True
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        db_table = "table_privacy_policy"
        verbose_name = "Privacy Policy"
        verbose_name_plural = "Privacy Policies"

    def __str__(self):
        if self.policy_heading_text:
            return self.policy_heading_text
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('dashboard:privacy-policy', args=[str(self.pk)])


class Banner(TimestampedModel):
    banner_id = models.BigAutoField(primary_key=True, editable=False)
    banner_image = models.ImageField(upload_to='banners/')
    send_to_all = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='banner_countries', null=True,
                                blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    town = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=15, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'table_banners'
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def get_absolute_url(self):
        return reverse('dashboard:banner-list')


class TranslateData(TimestampedModel):
    data = models.CharField(max_length=150, null=True, blank=True)
    translated = models.CharField(max_length=150, null=True, blank=True)
    afrikaans = models.CharField(max_length=150, null=True, blank=True)
    albanian = models.CharField(max_length=150, null=True, blank=True)
    amharic = models.CharField(max_length=150, null=True, blank=True)
    arabic = models.CharField(max_length=150, null=True, blank=True)
    armenian = models.CharField(max_length=150, null=True, blank=True)
    azerbaijani = models.CharField(max_length=150, null=True, blank=True)
    basque = models.CharField(max_length=150, null=True, blank=True)
    belarusian = models.CharField(max_length=150, null=True, blank=True)
    bengali = models.CharField(max_length=150, null=True, blank=True)
    bosnian = models.CharField(max_length=150, null=True, blank=True)
    bulgarian = models.CharField(max_length=150, null=True, blank=True)
    catalan = models.CharField(max_length=150, null=True, blank=True)
    cebuano = models.CharField(max_length=150, null=True, blank=True)
    chichewa = models.CharField(max_length=150, null=True, blank=True)
    chinese_simplified = models.CharField(max_length=150, null=True, blank=True)
    chinese_traditional = models.CharField(max_length=150, null=True, blank=True)
    corsican = models.CharField(max_length=150, null=True, blank=True)
    croatian = models.CharField(max_length=150, null=True, blank=True)
    czech = models.CharField(max_length=150, null=True, blank=True)
    danish = models.CharField(max_length=150, null=True, blank=True)
    dutch = models.CharField(max_length=150, null=True, blank=True)
    english = models.CharField(max_length=150, null=True, blank=True)
    esperanto = models.CharField(max_length=150, null=True, blank=True)
    estonian = models.CharField(max_length=150, null=True, blank=True)
    filipino = models.CharField(max_length=150, null=True, blank=True)
    finnish = models.CharField(max_length=150, null=True, blank=True)
    french = models.CharField(max_length=150, null=True, blank=True)
    frisian = models.CharField(max_length=150, null=True, blank=True)
    galician = models.CharField(max_length=150, null=True, blank=True)
    georgian = models.CharField(max_length=150, null=True, blank=True)
    german = models.CharField(max_length=150, null=True, blank=True)
    greek = models.CharField(max_length=150, null=True, blank=True)
    gujarati = models.CharField(max_length=150, null=True, blank=True)
    haitian_creole = models.CharField(max_length=150, null=True, blank=True)
    hausa = models.CharField(max_length=150, null=True, blank=True)
    hawaiian = models.CharField(max_length=150, null=True, blank=True)
    hebrew = models.CharField(max_length=150, null=True, blank=True)
    hebrew = models.CharField(max_length=150, null=True, blank=True)
    hindi = models.CharField(max_length=150, null=True, blank=True)
    hmong = models.CharField(max_length=150, null=True, blank=True)
    hungarian = models.CharField(max_length=150, null=True, blank=True)
    icelandic = models.CharField(max_length=150, null=True, blank=True)
    igbo = models.CharField(max_length=150, null=True, blank=True)
    indonesian = models.CharField(max_length=150, null=True, blank=True)
    irish = models.CharField(max_length=150, null=True, blank=True)
    italian = models.CharField(max_length=150, null=True, blank=True)
    japanese = models.CharField(max_length=150, null=True, blank=True)
    javanese = models.CharField(max_length=150, null=True, blank=True)
    kannada = models.CharField(max_length=150, null=True, blank=True)
    kazakh = models.CharField(max_length=150, null=True, blank=True)
    khmer = models.CharField(max_length=150, null=True, blank=True)
    korean = models.CharField(max_length=150, null=True, blank=True)
    kurdish_kurmanji = models.CharField(max_length=150, null=True, blank=True)
    kyrgyz = models.CharField(max_length=150, null=True, blank=True)
    lao = models.CharField(max_length=150, null=True, blank=True)
    latin = models.CharField(max_length=150, null=True, blank=True)
    latvian = models.CharField(max_length=150, null=True, blank=True)
    lithuanian = models.CharField(max_length=150, null=True, blank=True)
    luxembourgish = models.CharField(max_length=150, null=True, blank=True)
    macedonian = models.CharField(max_length=150, null=True, blank=True)
    malagasy = models.CharField(max_length=150, null=True, blank=True)
    malay = models.CharField(max_length=150, null=True, blank=True)
    malayalam = models.CharField(max_length=150, null=True, blank=True)
    maltese = models.CharField(max_length=150, null=True, blank=True)
    maori = models.CharField(max_length=150, null=True, blank=True)
    marathi = models.CharField(max_length=150, null=True, blank=True)
    mongolian = models.CharField(max_length=150, null=True, blank=True)
    myanmar_burmese = models.CharField(max_length=150, null=True, blank=True)
    nepali = models.CharField(max_length=150, null=True, blank=True)
    norwegian = models.CharField(max_length=150, null=True, blank=True)
    odia = models.CharField(max_length=150, null=True, blank=True)
    pashto = models.CharField(max_length=150, null=True, blank=True)
    persian = models.CharField(max_length=150, null=True, blank=True)
    polish = models.CharField(max_length=150, null=True, blank=True)
    portuguese = models.CharField(max_length=150, null=True, blank=True)
    punjabi = models.CharField(max_length=150, null=True, blank=True)
    romanian = models.CharField(max_length=150, null=True, blank=True)
    russian = models.CharField(max_length=150, null=True, blank=True)
    samoan = models.CharField(max_length=150, null=True, blank=True)
    scots_gaelic = models.CharField(max_length=150, null=True, blank=True)
    serbian = models.CharField(max_length=150, null=True, blank=True)
    sesotho = models.CharField(max_length=150, null=True, blank=True)
    shona = models.CharField(max_length=150, null=True, blank=True)
    sindhi = models.CharField(max_length=150, null=True, blank=True)
    sinhala = models.CharField(max_length=150, null=True, blank=True)
    slovak = models.CharField(max_length=150, null=True, blank=True)
    slovenian = models.CharField(max_length=150, null=True, blank=True)
    somali = models.CharField(max_length=150, null=True, blank=True)
    spanish = models.CharField(max_length=150, null=True, blank=True)
    sundanese = models.CharField(max_length=150, null=True, blank=True)
    swahili = models.CharField(max_length=150, null=True, blank=True)
    swedish = models.CharField(max_length=150, null=True, blank=True)
    tajik = models.CharField(max_length=150, null=True, blank=True)
    tamil = models.CharField(max_length=150, null=True, blank=True)
    telugu = models.CharField(max_length=150, null=True, blank=True)
    thai = models.CharField(max_length=150, null=True, blank=True)
    turkish = models.CharField(max_length=150, null=True, blank=True)
    ukrainian = models.CharField(max_length=150, null=True, blank=True)
    urdu = models.CharField(max_length=150, null=True, blank=True)
    uyghur = models.CharField(max_length=150, null=True, blank=True)
    uzbek = models.CharField(max_length=150, null=True, blank=True)
    vietnamese = models.CharField(max_length=150, null=True, blank=True)
    welsh = models.CharField(max_length=150, null=True, blank=True)
    xhosa = models.CharField(max_length=150, null=True, blank=True)
    iddish = models.CharField(max_length=150, null=True, blank=True)
    yoruba = models.CharField(max_length=150, null=True, blank=True)
    zulu = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'table_translate'
        verbose_name = "Translate"
        verbose_name_plural = "Translate"


# class LanguageData(TimestampedModel):
#     language = models.CharField(max_length=150, null=True, blank=True)
#     language_abbreviation = models.CharField(max_length=150, null=True, blank=True)
#
#     def __str__(self):
#         return str(self.pk)
#
#     class Meta:
#         db_table = 'table_languages'
#         verbose_name = "language"
#         verbose_name_plural = "language"

class Faqs(TimestampedModel):
    question = models.TextField()
    answer = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        db_table = "table_faqs"


class TranslatedUser(TimestampedModel):
    cook_pk = models.CharField(max_length=14, unique=True, null=True, blank=True)
    cook_id = models.CharField(max_length=14, unique=True, null=True, blank=True)
    courier_pk = models.CharField(max_length=14, unique=True, null=True, blank=True)
    courier_id = models.CharField(max_length=14, unique=True, null=True, blank=True)
    customer_pk = models.CharField(max_length=14, unique=True, null=True, blank=True)
    customer_id = models.CharField(max_length=14, unique=True, null=True, blank=True)
    language = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        db_table = "table_transalted_user"


class LandingPageContent(TimestampedModel):
    cook_heading = models.CharField(max_length=150, null=True, blank=True)
    cook_body = models.CharField(max_length=300, null=True, blank=True)
    courier_heading = models.CharField(max_length=150, null=True, blank=True)
    courier_body = models.CharField(max_length=300, null=True, blank=True)
    customer_heading = models.CharField(max_length=150, null=True, blank=True)
    customer_body = models.CharField(max_length=300, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        db_table = 'table_landing_page_content'

    def __str__(self):
        return self.cook_heading
