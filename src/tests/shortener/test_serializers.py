from analytics.models import Visit
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from shortener.models import ShortenedURL
from shortener.serializers import ShortenedURLSerializer


class ShortenedURLSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.request = cls.factory.get("/")

        cls.shortened_url = ShortenedURL.objects.create(
            original_url="https://example.com",
            short_code="testcode",
            creator_ip="127.0.0.1",
            creator_user_agent="Test User Agent",
        )

        Visit.objects.create(
            shortened_url=cls.shortened_url,
            ip_address="192.168.1.1",
        )
        Visit.objects.create(
            shortened_url=cls.shortened_url,
            ip_address="192.168.1.2",
        )

    def test_serializer_contains_expected_fields(self):
        """Test that the serializer includes all expected fields"""
        serializer = ShortenedURLSerializer(
            instance=self.shortened_url, context={"request": self.request}
        )
        data = serializer.data

        expected_fields = [
            "id",
            "original_url",
            "short_code",
            "short_url",
            "created_at",
            "creator_ip",
            "creator_user_agent",
            "stats_url",
        ]

        for field in expected_fields:
            self.assertIn(field, data)

    def test_get_short_url_with_request(self):
        """Test that get_short_url returns the correct URL with request context"""
        serializer = ShortenedURLSerializer(
            instance=self.shortened_url, context={"request": self.request}
        )

        expected_url = f"{self.request.build_absolute_uri('/')}{self.shortened_url.short_code}"
        self.assertEqual(serializer.data["short_url"], expected_url)

    def test_get_short_url_without_request(self):
        """Test that get_short_url returns a relative URL without request context"""
        serializer = ShortenedURLSerializer(instance=self.shortened_url)

        expected_url = f"/{self.shortened_url.short_code}"
        self.assertEqual(serializer.data["short_url"], expected_url)

    def test_get_stats_url_with_request(self):
        """Test that get_stats_url returns the correct URL with request context"""
        serializer = ShortenedURLSerializer(
            instance=self.shortened_url, context={"request": self.request}
        )

        stats_path = reverse("url-stats", kwargs={"short_code": self.shortened_url.short_code})
        expected_url = self.request.build_absolute_uri(stats_path)

        self.assertEqual(serializer.data["stats_url"], expected_url)

    def test_get_stats_url_without_request(self):
        """Test that get_stats_url returns a relative URL without request context"""
        serializer = ShortenedURLSerializer(instance=self.shortened_url)

        stats_path = reverse("url-stats", kwargs={"short_code": self.shortened_url.short_code})

        self.assertEqual(serializer.data["stats_url"], stats_path)

    def test_serializer_read_only_fields(self):
        """Test that read-only fields cannot be set through the serializer"""
        data = {
            "original_url": "https://example.com",
            "short_code": "attempted-override",
            "short_url": "attempted-override",
            "stats_url": "attempted-override",
        }

        serializer = ShortenedURLSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        # Only original_url should be in validated_data
        self.assertEqual(len(serializer.validated_data), 1)
        self.assertEqual(serializer.validated_data["original_url"], "https://example.com")
