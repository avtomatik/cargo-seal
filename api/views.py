from core.constants import SHEET_NAMES_EXPECTED
from core.services import (ExcelReader, assign_index_by_row_count,
                           clean_summary_dataframe,
                           standardize_dataset)
from coverage.models import Coverage, Policy
from logistics.models import Shipment
from pydantic_models.extractors import FieldExtractor
from pydantic_models.shipment_builders import ShipmentFactory
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from vessels.models import Document, Vessel

from api.serializers import (CoverageSerializer, DocumentSerializer,
                             FormMergeSerializer, PolicySerializer,
                             VesselSerializer)


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

        reader = ExcelReader()
        sheet_names, operator = reader.get_details(file)

        if not SHEET_NAMES_EXPECTED.issubset(sheet_names):
            print(
                f'Missing required sheets in {file.name}. Found: {sheet_names}'
            )
            return None

        try:
            df_summary = (
                reader.read_sheet(file, 'declaration_form')
                .pipe(assign_index_by_row_count)
                .pipe(clean_summary_dataframe)
            )
        except ValueError:
            print(
                f'Invalid declaration_form in {file.name} by {operator}')
            return None

        try:
            df_details = (
                reader.read_sheet(file, 'bl_breakdown')
                .pipe(standardize_dataset)
            )
        except ValueError:
            print(f'Invalid bl_breakdown in {file.name} by {operator}')
            return None

        shipment_factory = ShipmentFactory(extractor=FieldExtractor())

        shipment = shipment_factory.create(df_summary, df_details, operator)

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
