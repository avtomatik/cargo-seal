from rest_framework import serializers

from coverage.models import Coverage, Policy
from procurement.models import Party
from vessels.models import Document, Vessel


class PolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = Policy
        fields = '__all__'


class CoverageSerializer(serializers.ModelSerializer):

    policy = PolicySerializer()
    premium = serializers.ReadOnlyField()

    class Meta:
        model = Coverage
        fields = [
            'shipment',
            'policy',
            'debit_note',
            'date',
            'ordinary_risks_rate',
            'war_risks_rate',
            'premium'
        ]


class FormFieldsSerializer(serializers.Serializer):

    deal_number = serializers.CharField(max_length=16)
    insured = serializers.CharField(max_length=16)
    address = serializers.CharField(max_length=16)
    beneficiary = serializers.CharField(max_length=16)
    beneficiary_address = serializers.CharField(max_length=16)
    surveyor_disport = serializers.CharField(max_length=16)
    surveyor_loadport = serializers.CharField(max_length=16)
    basis_of_valuation = serializers.CharField(max_length=16)
    date = serializers.CharField(max_length=16)
    bl_number = serializers.CharField(max_length=16)
    bl_date = serializers.CharField(max_length=16)
    disport = serializers.CharField(max_length=16)
    loadport = serializers.CharField(max_length=16)
    policy_number = serializers.CharField(max_length=16)
    policy_date = serializers.CharField(max_length=16)
    subject_matter_insured = serializers.CharField(max_length=16)
    vessel = serializers.CharField(max_length=16)
    imo = serializers.CharField(max_length=16)
    year_built = serializers.CharField(max_length=16)
    sum_insured = serializers.CharField(max_length=16)
    weight_metric = serializers.CharField(max_length=16)


class PartySerializer(serializers.ModelSerializer):

    class Meta:
        model = Party
        fields = ['name']


class VesselSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vessel
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):

    vessel = VesselSerializer()
    provider = PartySerializer()
    is_valid = serializers.ReadOnlyField()

    class Meta:
        model = Document
        fields = '__all__'
