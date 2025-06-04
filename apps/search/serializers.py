from rest_framework import serializers
from apps.search.models import SearchQuery
from apps.rent.serializers import OfferSerializer

class SearchQuerySerializer(serializers.ModelSerializer):
    filters = serializers.JSONField()

    class Meta:
        model = SearchQuery
        fields = ['id', 'user', 'query', 'filters', 'created_at']

class SearchResultSerializer(OfferSerializer):
    class Meta(OfferSerializer.Meta):
        fields = OfferSerializer.Meta.fields