import json
import re

import pandas as pd
from django.conf import settings
from openpyxl import load_workbook
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
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
    parser_classes = [FormParser, MultiPartParser]

    @action(methods=['post'], detail=False)
    def submit(self, request):
        # =====================================================================
        # curl -X POST -F "file=@path/to/file;type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" http://localhost:8000/api/coverage/submit/
        # =====================================================================
        # =====================================================================
        # TODO: Make It Clear
        # =====================================================================
        file = request.data.get('file')
        if file:
            sheet_names, last_modified_by = self.extract_workbook_data(file)
            df_frm = pd.read_excel(
                file,
                sheet_name='declaration_form',
                names=('headers', 'current'),
                index_col=0,
                skiprows=1,
                skipfooter=2,
            ).transpose()

            df_frm.columns = map(
                lambda _: self.trim_string(_, '_').lower(), df_frm.columns
            )

            with open(settings.BASE_DIR.joinpath('data').joinpath('columns.json')) as file:
                COLUMNS_ALL = json.load(file)

            if all(x == y for x, y in zip(df_frm.columns, COLUMNS_ALL['Version 2023-05-12']['expected'])):
                df_frm.columns = COLUMNS_ALL['Version 2023-05-12']['fitted']

            data = df_frm.loc['current'].to_dict()
            data['operator'] = last_modified_by
            data.pop('_', None)

        # =====================================================================
        # TODO: Validate
        # =====================================================================
            return Response({'data': data}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def extract_workbook_data(self, file):
        wb = load_workbook(file, read_only=True, keep_links=False)
        sheet_names = wb.sheetnames
        last_modified_by = wb.properties.lastModifiedBy
        wb.close()
        return sheet_names, last_modified_by

    def trim_string(self, string: str, fill: str = ' ', char: str = r'\W') -> str:
        return fill.join(filter(bool, re.split(char, string)))


class VesselViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer
