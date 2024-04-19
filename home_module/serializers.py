from rest_framework import serializers

from home_module.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = Country.get_list_fields()
        read_only_fields = ['url', 'slug']
