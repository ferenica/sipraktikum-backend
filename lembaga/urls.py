from django.urls import path, include
from lembaga.views import LembagaView, InstitusiView, TemaView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('lembaga', LembagaView, basename="lembaga")
router.register('institusi', InstitusiView, basename="institusi")
router.register('tema', TemaView, basename="tema")

urlpatterns = [
    path('', include(router.urls)),
]
