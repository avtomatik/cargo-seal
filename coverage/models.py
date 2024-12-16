from django.db import models


class Coverage(models.Model):

    provider = models.ForeignKey(
        'Entity',
        on_delete=models.CASCADE,
        verbose_name='Underwriter',
        blank=True,
        null=True
    )
    reference = models.CharField(
        verbose_name='Underwriter`s Risk Reference',
        default='#'
    )
    invoice_number = models.CharField(
        verbose_name='Underwriter`s Invoice Reference',
        default='#'
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name='Date Risk Processed'
    )
    sum_insured = models.FloatField(
        verbose_name='Sum Insured'
    )  # TODO: Make It Calculated Field
    ordinary_risks_rate = models.FloatField(
        verbose_name='Standard Coverage Rate',
        default=.0
    )
    war_risks_rate = models.FloatField(
        verbose_name='War Risks Rate',
        default=.0
    )


class Entity(models.Model):

    name = models.CharField(verbose_name='Entity`s Name')
    address = models.CharField(verbose_name='Entity`s Title')


class Location(models.Model):

    locality = models.CharField(verbose_name='Port Locality')
    country = models.CharField(verbose_name='Port Country')


class Operator(models.Model):

    first_name = models.CharField(verbose_name='First Name')
    last_name = models.CharField(verbose_name='Last Name')


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
    volume = models.FloatField(verbose_name='Volume for Fluid Cargo, bbl')
    weight = models.FloatField(verbose_name='Weight, MT')
    loadport = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='parcels',
        verbose_name='Port of Loading'
    )
    disport = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='parcels',
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
    contract_number = models.CharField(verbose_name='Contract Number')
    ccy = models.CharField(verbose_name='Currency')
    unit = models.CharField()
    quote_per_unit = models.FloatField()
    subject_matter_insured = models.CharField()


class Vessel(models.Model):

    vessel = models.CharField()
    imo = models.PositiveIntegerField()
    date_built = models.DateField()
