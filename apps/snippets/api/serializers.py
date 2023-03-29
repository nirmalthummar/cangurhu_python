from rest_framework import serializers

from apps.snippets.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('country_id', 'country_name', 'iso2', 'iso3', 'isd_code', 'currency', 'flag', 'latitude', 'longitude')
