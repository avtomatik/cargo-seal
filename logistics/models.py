from django.db import models

from core.constants import (MAX_LENGTH_CCY, MAX_LENGTH_CHAR, MAX_LENGTH_TEXT,
                            MAX_LENGTH_UNIT)
from procurement.models import Contract, Party


class Location(models.Model):

    locality = models.CharField(
        verbose_name='Port Locality',
        max_length=MAX_LENGTH_CHAR
    )
    country = models.CharField(
        verbose_name='Port Country',
        max_length=MAX_LENGTH_CHAR
    )


class Operator(models.Model):

    first_name = models.CharField(
        verbose_name='First Name',
        max_length=MAX_LENGTH_CHAR
    )
    last_name = models.CharField(
        verbose_name='Last Name',
        max_length=MAX_LENGTH_CHAR
    )


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
    quantity = models.DecimalField(
        verbose_name='Quantity',
        decimal_places=6,
        max_digits=16
    )
    loadport = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        verbose_name='Port of Loading'
    )
    disport = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        verbose_name='Port of Discharge'
    )
    surveyor_loadport = models.ForeignKey(
        Party,
        on_delete=models.CASCADE,
        verbose_name='Surveyor Company at Port of Loading',
        blank=True,
        null=True
    )
    surveyor_disport = models.ForeignKey(
        Party,
        on_delete=models.CASCADE,
        verbose_name='Surveyor Company at Port of Discharge',
        blank=True,
        null=True
    )
    ccy = models.CharField(verbose_name='Currency', max_length=MAX_LENGTH_CCY)
    unit = models.CharField(max_length=MAX_LENGTH_UNIT)
    quote_per_unit = models.DecimalField(decimal_places=6, max_digits=12)
    subject_matter_insured = models.CharField(max_length=MAX_LENGTH_TEXT)
