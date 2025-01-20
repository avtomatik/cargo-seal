from rest_framework import serializers

from procurement.models import Party
from vessels.models import Document, Vessel


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
