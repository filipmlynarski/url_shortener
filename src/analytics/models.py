from django.db import models

from shortener.models import ShortenedURL


class Visit(models.Model):
    shortened_url = models.ForeignKey(
        ShortenedURL, on_delete=models.CASCADE, related_name="visit_logs"
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Visit to {self.shortened_url.short_code} at {self.created_at.isoformat()}"
