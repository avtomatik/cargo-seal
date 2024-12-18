from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Coverage(models.Model):

    provider = models.ForeignKey(
        'Entity',
        on_delete=models.SET_NULL,
        verbose_name='Underwriter',
        blank=True,
        null=True
    )
    reference = models.CharField(
        verbose_name='Underwriter`s Risk Reference',
        max_length=64,
        default='#'
    )
    invoice_number = models.CharField(
        verbose_name='Underwriter`s Invoice Reference',
        max_length=32,
        default='#'
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name='Date Risk Processed'
    )
    ordinary_risks_rate = models.DecimalField(
        verbose_name='Standard Coverage Rate',
        decimal_places=8,
        max_digits=9,
        default=.0
    )
    war_risks_rate = models.DecimalField(
        verbose_name='War Risks Rate',
        decimal_places=8,
        max_digits=9,
        default=.0
    )

    @property
    def sum_insured(self):
        return 1.0

    @property
    def premium(self):
        return 1.0


class Document(models.Model):

    class Category(models.TextChoices):
        CLASS_CERTIFICATE = 'class_certificate', _('Class Certificate')
        P_I_POLICY = 'p_i_policy', _('P & I Policy')

    category = models.CharField(
        blank=False,
        choices=Category.choices,
        max_length=32
    )
    vessel = models.ForeignKey(
        'Vessel',
        on_delete=models.CASCADE
    )
    provider = models.ForeignKey(
        'Entity',
        on_delete=models.SET_NULL,
        null=True
    )
    number = models.CharField(max_length=64)
    date = models.DateField()

    @property
    def is_valid(self):
        return timezone.now().date() >= self.date


class Entity(models.Model):

    name = models.CharField(verbose_name='Entity`s Name', max_length=256)
    address = models.CharField(verbose_name='Entity`s Title', max_length=256)


class Location(models.Model):

    locality = models.CharField(verbose_name='Port Locality', max_length=64)
    country = models.CharField(verbose_name='Port Country', max_length=64)


class Operator(models.Model):

    first_name = models.CharField(verbose_name='First Name', max_length=64)
    last_name = models.CharField(verbose_name='Last Name', max_length=64)


class Policy(models.Model):

    provider = models.ForeignKey('Entity', on_delete=models.CASCADE, related_name='underwriter')
    insured = models.ForeignKey('Entity', on_delete=models.CASCADE, related_name='policyholder')
    number = models.CharField(max_length=32)
    date = models.DateField()
    inception = models.DateTimeField()
    expiry = models.DateTimeField()


class Shipment(models.Model):

    trade = models.ForeignKey(
        'Trade',
        on_delete=models.CASCADE,
        related_name='parcels',
        verbose_name='General Trade'
    )
    operator = models.ForeignKey(
        Operator,
        on_delete=models.CASCADE,
        related_name='parcels',
        verbose_name='Trade'
    )
    bl_date = models.DateField(verbose_name='Bill of Lading Date')
    disport_eta = models.DateTimeField(
        verbose_name='Discharge Port ETA or NOR'
    )
    volume = models.DecimalField(
        verbose_name='Volume for Fluid Cargo, bbl',
        decimal_places=6,
        max_digits=16
    )
    weight = models.DecimalField(
        verbose_name='Weight, MT',
        decimal_places=6,
        max_digits=16
    )
    loadport = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='origin',
        verbose_name='Port of Loading'
    )
    disport = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='destination',
        verbose_name='Port of Discharge'
    )
    surveyor_loadport = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name='parcels',
        verbose_name='Surveyor Company at Port of Loading',
        blank=True,
        null=True
    )
    surveyor_disport = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name='parcels',
        verbose_name='Surveyor Company at Port of Discharge',
        blank=True,
        null=True
    )


class Trade(models.Model):

    number = models.PositiveIntegerField(verbose_name='Deal Number')
    insured = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name='trades',
        verbose_name='Company'
    )
    beneficiary = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name='trades',
        verbose_name='Counterparty'
    )
    contract_number = models.CharField(verbose_name='Contract Number', max_length=64)
    ccy = models.CharField(verbose_name='Currency', max_length=3)
    unit = models.CharField(max_length=16)
    quote_per_unit = models.DecimalField(decimal_places=6, max_digits=12)
    subject_matter_insured = models.CharField(max_length=256)


class Vessel(models.Model):

    vessel = models.CharField(max_length=32)
    imo = models.PositiveIntegerField()
    date_built = models.DateField()
