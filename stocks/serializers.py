from rest_framework import serializers
from .models import TrackedStock

class TrackedStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackedStock
        fields = ['tracked_stocks']