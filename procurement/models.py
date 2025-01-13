from django.db import models

from core.constants import MAX_LENGTH_CHAR, MAX_LENGTH_TEXT


class Contract(models.Model):

    number = models.CharField(
        verbose_name='Contract Number', max_length=MAX_LENGTH_CHAR)
    seller = models.ForeignKey(
        'Entity',
        on_delete=models.CASCADE,
        verbose_name='Selling Company'
    )
    buyer = models.ForeignKey(
        'Entity',
        on_delete=models.CASCADE,
        verbose_name='Buying Company'
    )


class Entity(models.Model):

    name = models.CharField(
        verbose_name='Entity`s Name',
        max_length=MAX_LENGTH_TEXT
    )
    address = models.CharField(
        verbose_name='Entity`s Title',
        max_length=MAX_LENGTH_TEXT
    )
