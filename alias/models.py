from django.db import models


class Alias(models.Model):
    target = models.URLField()
    alias = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = 'Aliases'
