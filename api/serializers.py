from django.utils import timezone
from rest_framework import serializers

from coverage.models import Coverage, Policy
from logistics.models import Shipment
from procurement.models import Party
from vessels.models import Document, Vessel


class BillOfLadingSerializer(serializers.Serializer):

    bl_number = serializers.CharField(source='number')

    class Meta:
        model = Shipment


class PolicySerializer(serializers.ModelSerializer):

    insured = serializers.CharField(source='insured.name')
    provider = serializers.CharField(source='provider.name')

    class Meta:
        model = Policy
        fields = ['number', 'provider', 'insured', 'expiry']


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


class FormMergeSerializer(serializers.Serializer):

    deal_number = serializers.CharField(source='number')
    insured = serializers.CharField(source='coverage.policy.insured')
    address = serializers.CharField(source='coverage.policy.insured.address')
    beneficiary = serializers.CharField(source='contract.buyer')
    beneficiary_address = serializers.CharField(
        source='contract.buyer.address'
    )
    surveyor_loadport = serializers.CharField(source='surveyor_loadport.name')
    surveyor_disport = serializers.CharField(source='surveyor_disport.name')
    basis_of_valuation = serializers.SerializerMethodField(read_only=True)
    date = serializers.SerializerMethodField(read_only=True)
    # bl_number = BillOfLadingSerializer(many=True)
# =============================================================================
#     TODO: Implement Handle to Generate the Following Output:
#         "bl_number": [
#             {
#                 "bl_number": "Bill of Lading #\u00a0SILNVS25117500 dated 19\u00a0March\u00a02025"
#             }
#         ],
# =============================================================================
    bl_date = serializers.SerializerMethodField(read_only=True)
    loadport = serializers.CharField(max_length=16)
    disport = serializers.CharField(max_length=16)
    policy_number = serializers.CharField(source='coverage.policy.number')
    policy_date = serializers.SerializerMethodField(read_only=True)
    subject_matter_insured = serializers.CharField(max_length=16)
    vessel = serializers.CharField(source='vessel.name')
    imo = serializers.CharField(source='vessel.imo')
    year_built = serializers.SerializerMethodField(read_only=True)
    weight_metric = serializers.SerializerMethodField(read_only=True)
    sum_insured = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Shipment
        fields = [
            'deal_number',
            'insured',
            'address',
            'beneficiary',
            'beneficiary_address',
            'surveyor_loadport',
            'surveyor_disport',
            'basis_of_valuation',
            'date',
            'bl_number',
            'bl_date',
            'loadport',
            'disport',
            'policy_number',
            'policy_date',
            'subject_matter_insured',
            'vessel',
            'imo',
            'year_built',
            'weight_metric',
            'sum_insured',
        ]

    def get_basis_of_valuation(self, obj):
        return '100%'

    def get_date(self, obj):
        today = timezone.now().date()
        return self.format_date(min(obj.date, today))

    def get_sum_insured(self, obj):
        return f'{obj.ccy} {float(obj.sum_insured):,.2f}'

    def get_weight_metric(self, obj):
        return f'{obj.weight_metric:,.3f}'

    def get_year_built(self, obj):
        return obj.vessel.built_on.year

    def get_bl_date(self, obj):
        return self.format_date(obj.date)

    def get_policy_date(self, obj):
        return self.format_date(obj.coverage.policy.inception)

    def format_date(self, date):
        return f'{date:%d\u00a0%B\u00a0%Y}' if date else None


class VesselSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vessel
        fields = ['name', 'imo', 'built_on']


class DocumentSerializer(serializers.ModelSerializer):

    vessel = VesselSerializer()
    provider = serializers.CharField(source='provider.name')
    is_valid = serializers.ReadOnlyField()

    class Meta:
        model = Document
        fields = [
            'vessel',
            'category',
            'provider',
            'number',
            'date',
            'is_valid'
        ]
