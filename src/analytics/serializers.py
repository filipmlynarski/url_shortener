from rest_framework import serializers

from analytics.models import Visit


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ["id", "ip_address", "created_at"]
        read_only_fields = ["id", "ip_address", "created_at"]


class URLStatsSerializer(serializers.Serializer):
    visit_details = VisitSerializer(many=True)
