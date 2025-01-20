from rest_framework import serializers

from procurement.models import Party
from vessels.models import Document, Vessel


class PartySerializer(serializers.ModelSerializer):

    class Meta:
        model = Party
        fields = '__all__'


class VesselSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vessel
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):

    vessel = VesselSerializer()
    provider = PartySerializer()

    class Meta:
        model = Document
        fields = '__all__'
