from django.db import models

from .constants import MAX_LENGTH_TEXT


class Entity(models.Model):

    name = models.CharField(
        verbose_name='Entity`s Name',
        max_length=MAX_LENGTH_TEXT
    )
    address = models.CharField(
        verbose_name='Entity`s Address',
        max_length=MAX_LENGTH_TEXT
    )

    class Meta:
        abstract = True
