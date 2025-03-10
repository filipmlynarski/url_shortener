from analytics.models import Visit
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shortener.models import ShortenedURL


class URLStatsViewTests(APITestCase):
    def setUp(self):
        self.shortened_url = ShortenedURL.objects.create(
            original_url="https://example.com",
            short_code="testcode",
            creator_ip="127.0.0.1",
            creator_user_agent="Test Creator Agent",
        )

        self.visit1 = Visit.objects.create(
            shortened_url=self.shortened_url,
        )
        self.visit2 = Visit.objects.create(
            shortened_url=self.shortened_url,
            ip_address="192.168.1.2",
        )

        self.url = reverse("url-stats", kwargs={"short_code": self.shortened_url.short_code})

    def test_get_url_stats_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertEqual(response.data["count"], 2)

        results = response.data["results"]
        self.assertIn("visit_details", results)
        self.assertEqual(len(results["visit_details"]), 2)

        visit = results["visit_details"][0]
        self.assertIn("id", visit)
        self.assertIn("ip_address", visit)
        self.assertIn("created_at", visit)

        self.assertEqual(results["visit_details"][0]["ip_address"], self.visit2.ip_address)
        self.assertEqual(results["visit_details"][1]["ip_address"], self.visit1.ip_address)

    def test_get_url_stats_not_found(self):
        url = reverse("url-stats", kwargs={"short_code": "nonexistent"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"].code, "not_found")

    def test_get_url_stats_with_no_visits(self):
        new_url = ShortenedURL.objects.create(
            original_url="https://example2.com", short_code="novisits"
        )

        url = reverse("url-stats", kwargs={"short_code": new_url.short_code})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertEqual(response.data["count"], 0)

        results = response.data["results"]
        self.assertIn("visit_details", results)
        self.assertEqual(len(results["visit_details"]), 0)

    def test_visit_logs_related_name(self):
        Visit.objects.create(
            shortened_url=self.shortened_url,
            ip_address="192.168.1.3",
        )

        response = self.client.get(self.url)
        self.assertIn("count", response.data)
        self.assertEqual(response.data["count"], 3)

        results = response.data["results"]
        self.assertIn("visit_details", results)
        self.assertEqual(len(results["visit_details"]), 3)

    def test_pagination(self):
        Visit.objects.bulk_create(
            [
                Visit(
                    shortened_url=self.shortened_url,
                    ip_address=f"192.168.1.{i}",
                )
                for i in range(3, 13)
            ]
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 12)
        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

        response = self.client.get(response.data["next"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["next"])
        self.assertIsNotNone(response.data["previous"])
