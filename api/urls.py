from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import VesselViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'vessels', VesselViewSet, basename='vessels')

urlpatterns = [
    path('', include(router.urls)),
]
