from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.constants import MAX_LENGTH_CHAR, MAX_LENGTH_REF
from procurement.models import Party


class Document(models.Model):

    class Category(models.TextChoices):
        CLASS_CERTIFICATE = 'class_certificate', _('Class Certificate')
        P_I_POLICY = 'p_i_policy', _('P & I Policy')

    number = models.CharField(max_length=MAX_LENGTH_CHAR)
    category = models.CharField(
        blank=False,
        choices=Category.choices,
        max_length=MAX_LENGTH_REF
    )
    vessel = models.ForeignKey(
        'Vessel',
        on_delete=models.CASCADE
    )
    provider = models.ForeignKey(
        Party,
        on_delete=models.SET_NULL,
        null=True
    )
    date = models.DateField()

    @property
    def is_valid(self):
        return timezone.now().date() >= self.date

    def __str__(self):
        return f'Ref # {self.number}'


class Vessel(models.Model):

    name = models.CharField(max_length=MAX_LENGTH_REF)
    imo = models.PositiveIntegerField()
    built_on = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'imo'],
                name='unique_name_imo'
            ),
            models.UniqueConstraint(
                fields=['imo', 'built_on'],
                name='unique_imo_date_built'
            )
        ]

    def __str__(self):
        return f'{self.name}, IMO: {self.imo}'
