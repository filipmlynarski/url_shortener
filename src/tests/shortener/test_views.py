from unittest.mock import patch

from analytics.models import Visit
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shortener.models import ShortenedURL


class ShortenedURLViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.list_url = reverse("shortenedurl-list")

        cls.shortened_url = ShortenedURL.objects.create(
            original_url="https://example.com",
            short_code="testcode",
            creator_ip="127.0.0.1",
            creator_user_agent="Test User Agent",
        )

        cls.detail_url = reverse(
            "shortenedurl-detail", kwargs={"short_code": cls.shortened_url.short_code}
        )

    @patch("shortener.views.ShortenedURL.create_short_code")
    def test_create_shortened_url(self, mock_create_short_code):
        """Test creating a new shortened URL"""
        mock_create_short_code.return_value = "newtestcode"

        data = {"original_url": "https://newexample.com"}
        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShortenedURL.objects.count(), 2)
        self.assertEqual(
            ShortenedURL.objects.get(original_url="https://newexample.com").original_url,
            "https://newexample.com",
        )

        self.assertIn("id", response.data)
        self.assertEqual(response.data["original_url"], "https://newexample.com")
        self.assertEqual(response.data["short_code"], "newtestcode")
        self.assertEqual(response.data["short_url"], "http://testserver/newtestcode")
        self.assertIn("created_at", response.data)
        self.assertIn("creator_ip", response.data)
        self.assertIn("creator_user_agent", response.data)
        self.assertEqual(
            response.data["stats_url"],
            "http://testserver/analytics/newtestcode/",
        )

    def test_create_duplicate_url(self):
        """Test creating a URL that already exists returns the existing one"""
        data = {"original_url": "https://example.com"}
        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ShortenedURL.objects.count(), 1)  # No new object created
        self.assertEqual(response.data["short_code"], self.shortened_url.short_code)

    def test_list_shortened_urls(self):
        """Test listing all shortened URLs"""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["short_code"], self.shortened_url.short_code)

        # Check pagination metadata
        self.assertIn("count", response.data)
        self.assertEqual(response.data["count"], 1)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

    def test_pagination(self):
        """Test that pagination works correctly"""
        for i in range(15):
            ShortenedURL.objects.create(
                original_url=f"https://example{i}.com",
                short_code=f"testcode{i}",
                creator_ip="127.0.0.1",
                creator_user_agent="Test User Agent",
            )

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertEqual(response.data["count"], 16)
        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

        response = self.client.get(response.data["next"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 6)
        self.assertIsNone(response.data["next"])
        self.assertIsNotNone(response.data["previous"])

    def test_retrieve_shortened_url(self):
        """Test retrieving a specific shortened URL"""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["short_code"], self.shortened_url.short_code)
        self.assertEqual(response.data["original_url"], self.shortened_url.original_url)

    def test_update_shortened_url(self):
        """Test updating a shortened URL"""
        data = {"original_url": "https://updated-example.com"}
        response = self.client.put(self.detail_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.shortened_url.refresh_from_db()
        self.assertEqual(self.shortened_url.original_url, "https://updated-example.com")

    def test_delete_shortened_url(self):
        """Test deleting a shortened URL"""
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ShortenedURL.objects.count(), 0)


class RedirectViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.shortened_url = ShortenedURL.objects.create(
            original_url="https://example.com",
            short_code="testcode",
            creator_ip="127.0.0.1",
            creator_user_agent="Test User Agent",
        )

        cls.redirect_url = reverse(
            "redirect_to_original", kwargs={"short_code": cls.shortened_url.short_code}
        )

    def test_redirect_to_original(self):
        """Test redirecting to the original URL"""
        response = self.client.get(self.redirect_url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, self.shortened_url.original_url)

        # Check that a visit was recorded
        self.assertEqual(Visit.objects.count(), 1)
        visit = Visit.objects.first()
        self.assertEqual(visit.shortened_url, self.shortened_url)

    def test_redirect_nonexistent_url(self):
        """Test redirecting with a non-existent short code"""
        url = reverse("redirect_to_original", kwargs={"short_code": "nonexistent"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_multiple_visits_recorded(self):
        """Test that multiple visits to the same URL are recorded"""
        # Visit the URL twice
        self.client.get(self.redirect_url)
        self.client.get(self.redirect_url)

        # Check that two visits were recorded
        self.assertEqual(Visit.objects.count(), 2)
        visits = Visit.objects.all()
        for visit in visits:
            self.assertEqual(visit.shortened_url, self.shortened_url)
