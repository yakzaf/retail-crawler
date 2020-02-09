from rest_framework import serializers
from web_scraper.models import HmTable


class HmItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HmTable
        fields = ('title', 'item_link', 'regular_price', 'sale_price')
