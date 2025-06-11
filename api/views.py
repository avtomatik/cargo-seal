from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from api.serializers import (CoverageSerializer, DocumentSerializer,
                             FormMergeSerializer, PolicySerializer,
                             VesselSerializer)
from core.services import process_shipment_file
from coverage.models import Coverage, Policy
from logistics.models import Shipment
from vessels.models import Document, Vessel


class CoverageViewSet(viewsets.ModelViewSet):

    queryset = Coverage.objects.all()
    serializer_class = CoverageSerializer
    parser_classes = [FormParser, MultiPartParser]

    @action(methods=['get', 'post'], detail=True)
    def draft(self, request):
        if request.method == 'GET':
            # TODO: Implement: Produce Coverage Documents
            return Response(
                {'message': 'This Endpoint Functionality Is Under Construction'},
                status=status.HTTP_200_OK
            )
        if request.method == 'POST':
            # TODO: Implement: Translate Form to Documents
            return Response(
                {'message': 'This Endpoint Functionality Is Under Construction'},
                status=status.HTTP_200_OK
            )

    @action(methods=['post'], detail=False)
    def push(self, request):
        """Push Declaration to Database Handler."""
        # =====================================================================
        # TODO: Make It Clear
        # =====================================================================
        file = request.data.get('file')

        if not file:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        shipment = process_shipment_file(file)

        if shipment is None:
            return Response(
                {'error': 'Failed to process shipment file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(shipment.model_dump_json(), status=status.HTTP_200_OK)


class FormMergeViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Shipment.objects.all()
    serializer_class = FormMergeSerializer


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class PolicyViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Policy.objects.all()
    serializer_class = PolicySerializer


class VesselViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer

    @action(methods=['post'], detail=True)
    def check(self, request):
        # TODO: Implement
        return Response(
            {'message': 'This Endpoint Functionality Is Under Construction'},
            status=status.HTTP_200_OK
        )
