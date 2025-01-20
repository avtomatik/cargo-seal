from rest_framework import serializers

from vessels.models import Document, Vessel


class VesselSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vessel
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):

    vessel = VesselSerializer()

    class Meta:
        model = Document
        fields = '__all__'
