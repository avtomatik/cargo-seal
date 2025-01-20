from rest_framework import viewsets

from api.serializers import VesselSerializer
from vessels.models import Document, Vessel


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class VesselViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer
