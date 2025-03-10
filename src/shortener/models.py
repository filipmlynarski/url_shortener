import random
import string

from django.conf import settings
from django.db import models


class ShortCodeGeneratorError(Exception):
    pass


class ShortenedURL(models.Model):
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=20, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator_ip = models.GenericIPAddressField(null=True, blank=True)
    creator_user_agent = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.short_code} -> {self.original_url}"

    @classmethod
    def create_short_code(cls, length=None):
        if length is None:
            length = getattr(settings, "URL_SHORTENER_LENGTH", 6)

        existing_short_codes = set(cls.objects.values_list("short_code", flat=True))
        chars = string.ascii_letters + string.digits
        for _ in range(1_000):
            short_code = "".join(random.choice(chars) for _ in range(length))
            if short_code not in existing_short_codes:
                return short_code
        raise ShortCodeGeneratorError("Failed to generate a unique short code")
