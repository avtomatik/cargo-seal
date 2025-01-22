from django.db import models

from core.constants import (MAX_LENGTH_CCY, MAX_LENGTH_CHAR, MAX_LENGTH_TEXT,
                            MAX_LENGTH_UNIT)
from procurement.models import Contract, Party


class Location(models.Model):

    name = models.CharField(
        verbose_name='Port Locality',
        max_length=MAX_LENGTH_CHAR
    )
    country = models.CharField(
        verbose_name='Port Country',
        max_length=MAX_LENGTH_CHAR
    )

    def __str__(self):
        return self.name


class Operator(models.Model):

    first_name = models.CharField(
        verbose_name='First Name',
        max_length=MAX_LENGTH_CHAR
    )
    last_name = models.CharField(
        verbose_name='Last Name',
        max_length=MAX_LENGTH_CHAR
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Shipment(models.Model):

    number = models.PositiveIntegerField(verbose_name='Deal Number')
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        verbose_name='Sell Contract'
    )
    operator = models.ForeignKey(
        Operator,
        on_delete=models.CASCADE,
        verbose_name='Operator'
    )
    date = models.DateField(verbose_name='Bill of Lading Date, Roughly')
    disport_eta = models.DateTimeField(
        verbose_name='Discharge Port ETA or NOR'
    )
    loadport = models.ForeignKey(
        Location,
        related_name='loadport_shipments',
        on_delete=models.CASCADE,
        verbose_name='Port of Loading'
    )
    disport = models.ForeignKey(
        Location,
        related_name='disport_shipments',
        on_delete=models.CASCADE,
        verbose_name='Port of Discharge'
    )
    surveyor_loadport = models.ForeignKey(
        Party,
        related_name='loadport_surveyors',
        on_delete=models.CASCADE,
        verbose_name='Surveyor Company at Port of Loading',
        blank=True,
        null=True
    )
    surveyor_disport = models.ForeignKey(
        Party,
        related_name='disport_surveyors',
        on_delete=models.CASCADE,
        verbose_name='Surveyor Company at Port of Discharge',
        blank=True,
        null=True
    )
    ccy = models.CharField(verbose_name='Currency', max_length=MAX_LENGTH_CCY)
    unit = models.CharField(max_length=MAX_LENGTH_UNIT, default='bbl')
    volume_bbl = models.DecimalField(
        verbose_name='Quantity, bbl',
        decimal_places=6,
        max_digits=16
    )
    weight_metric = models.DecimalField(
        verbose_name='Quantity, MT',
        decimal_places=6,
        max_digits=16
    )
    subject_matter_insured = models.CharField(max_length=MAX_LENGTH_TEXT)

# =============================================================================
# TODO: Introduce The Below Fields Later:
# =============================================================================
# =============================================================================
#     quantity = models.DecimalField(
#         verbose_name='Quantity',
#         decimal_places=6,
#         max_digits=16
#     )
#     quote_per_unit = models.DecimalField(decimal_places=6, max_digits=12)
# =============================================================================

    def __str__(self):
        return f'Deal # {self.number}'
