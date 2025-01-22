from openpyxl import load_workbook
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
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
    parser_classes = [FileUploadParser]

    @action(methods=['post'], detail=False)
    def submit(self, request):
        # =====================================================================
        # TODO: Request:
        # curl -X POST -F "file=@path/to/file;type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" http://localhost:8000/api/coverage/submit/
        # Fails with Message:
        # {"detail":"Missing filename. Request should include a Content-Disposition header with a filename parameter."}
        # =====================================================================
        file = request.data.get('file')
        if file:
            workbook = load_workbook(file, read_only=True, keep_links=False)
            sheet_names = workbook.sheetnames
            last_modified_by = workbook.properties.lastModifiedBy
            return Response(
                {
                    'message': 'Form Received',
                    'data': {
                        'sheet_names': sheet_names,
                        'operator': last_modified_by
                    }
                },
                status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VesselViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer
