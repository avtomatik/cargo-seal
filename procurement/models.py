from django.db import models

from core.constants import MAX_LENGTH_CHAR
from core.models import Entity


class Contract(models.Model):

    number = models.CharField(
        verbose_name='Contract Number',
        max_length=MAX_LENGTH_CHAR
    )
    seller = models.ForeignKey(
        'Party',
        related_name='seller_contracts',
        on_delete=models.CASCADE,
        verbose_name='Selling Company'
    )
    buyer = models.ForeignKey(
        'Party',
        related_name='buyer_contracts',
        on_delete=models.CASCADE,
        verbose_name='Buying Company'
    )

    def __str__(self):
        return f'Contract # {self.number}'


class Party(Entity):

    def __str__(self):
        return self.name
