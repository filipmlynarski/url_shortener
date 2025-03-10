from analytics.models import Visit
from analytics.serializers import URLStatsSerializer, VisitSerializer
from django.test import TestCase

from shortener.models import ShortenedURL


class VisitSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.shortened_url = ShortenedURL.objects.create(
            original_url="https://example.com",
            short_code="testcode",
            creator_ip="127.0.0.1",
            creator_user_agent="Test Creator Agent",
        )

        cls.visit = Visit.objects.create(
            shortened_url=cls.shortened_url,
            ip_address="192.168.1.1",
        )

    def test_visit_serializer_contains_expected_fields(self):
        """Test that VisitSerializer contains expected fields"""
        serializer = VisitSerializer(instance=self.visit)
        data = serializer.data

        self.assertIn("id", data)
        self.assertIn("ip_address", data)
        self.assertIn("created_at", data)

        self.assertEqual(data["ip_address"], "192.168.1.1")

    def test_visit_serializer_with_null_fields(self):
        """Test that VisitSerializer handles null fields correctly"""
        # Create a visit with null fields (which are allowed in the model)
        visit_with_nulls = Visit.objects.create(shortened_url=self.shortened_url, ip_address=None)

        serializer = VisitSerializer(instance=visit_with_nulls)
        data = serializer.data

        self.assertIsNone(data["ip_address"])


class URLStatsSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.shortened_url = ShortenedURL.objects.create(
            original_url="https://example.com",
            short_code="testcode",
            creator_ip="127.0.0.1",
            creator_user_agent="Test Creator Agent",
        )

        cls.visit1 = Visit.objects.create(
            shortened_url=cls.shortened_url,
            ip_address="192.168.1.1",
        )
        cls.visit2 = Visit.objects.create(
            shortened_url=cls.shortened_url,
            ip_address="192.168.1.2",
        )

        cls.visits = cls.shortened_url.visit_logs.all()
        cls.stats_data = {
            "visit_details": cls.visits,
        }

    def test_url_stats_serializer(self):
        """Test that URLStatsSerializer correctly serializes data"""
        serializer = URLStatsSerializer(self.stats_data)
        data = serializer.data

        self.assertEqual(len(data["visit_details"]), 2)

        visit_detail = data["visit_details"][0]
        self.assertIn("id", visit_detail)
        self.assertIn("ip_address", visit_detail)
        self.assertIn("created_at", visit_detail)

    def test_url_stats_serializer_respects_ordering(self):
        """Test that URLStatsSerializer respects the Visit model's ordering"""
        serializer = URLStatsSerializer(self.stats_data)
        data = serializer.data

        self.assertEqual(data["visit_details"][0]["ip_address"], self.visit1.ip_address)
        self.assertEqual(data["visit_details"][1]["ip_address"], self.visit2.ip_address)

    def test_url_stats_serializer_with_empty_visits(self):
        """Test that URLStatsSerializer handles empty visit lists correctly"""
        # Create a new URL with no visits
        new_url = ShortenedURL.objects.create(
            original_url="https://example2.com", short_code="novisits"
        )

        empty_visits = new_url.visit_logs.all()
        stats_data = {
            "visit_details": empty_visits,
        }

        serializer = URLStatsSerializer(stats_data)
        data = serializer.data

        self.assertEqual(len(data["visit_details"]), 0)
