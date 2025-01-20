from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (CoverageSerializer, DocumentSerializer,
                             VesselSerializer)
from coverage.models import Coverage
from vessels.models import Document, Vessel


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class CoverageViewSet(viewsets.ModelViewSet):

    queryset = Coverage.objects.all()
    serializer_class = CoverageSerializer
    parser_classes = [None]

    @action(methods=['post'], detail=False)
    def submit(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)


class VesselViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer
