from django.db import models

from core.constants import MAX_LENGTH_SLUG

from .constants import MAX_LENGTH_TEXT

from django.utils.text import slugify


class Entity(models.Model):

    name = models.CharField(
        verbose_name="Entity’s Name",
        max_length=MAX_LENGTH_TEXT,
        unique=True,
        db_index=True
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        blank=True,
        help_text="URL-safe identifier auto-generated from name"
    )
    address = models.CharField(
        verbose_name="Entity’s Address",
        max_length=MAX_LENGTH_TEXT
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
