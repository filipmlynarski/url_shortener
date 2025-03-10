from django.urls import reverse
from rest_framework import serializers

from shortener.models import ShortenedURL


class ShortenedURLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    stats_url = serializers.SerializerMethodField()

    class Meta:
        model = ShortenedURL
        fields = [
            "id",
            "original_url",
            "short_code",
            "short_url",
            "created_at",
            "creator_ip",
            "creator_user_agent",
            "stats_url",
        ]
        read_only_fields = [
            "id",
            "short_code",
            "short_url",
            "created_at",
            "creator_ip",
            "creator_user_agent",
            "stats_url",
        ]

    def get_short_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/{obj.short_code}")
        return f"/{obj.short_code}"

    def get_stats_url(self, obj):
        stats_path = reverse("url-stats", kwargs={"short_code": obj.short_code})
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(stats_path)
        return stats_path
