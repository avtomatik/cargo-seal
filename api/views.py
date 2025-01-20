from rest_framework import viewsets

from api.serializers import VesselSerializer
from vessels.models import Vessel


class VesselViewSet(viewsets.ModelViewSet):

    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer
