from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from lembaga.models import Lembaga, Institusi, Tema
from lembaga.serializers import LembagaSerializer, InstitusiSerializer, TemaSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class LembagaView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = LembagaSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a query parameter in the URL.
        """
        try:
            queryset = Lembaga.objects.all()
            param_institusi = self.request.GET.get('institusi')
            param_tema = self.request.GET.get('tema')
            param_praktikum = self.request.GET.get('praktikum')
            param_nama = self.request.GET.get('nama')

            if param_praktikum:
                temp = param_praktikum.split(',')
                param_praktikum = []
                for i in temp:
                    param_praktikum.append(int(i[-1]))
                queryset = queryset.filter(praktikum_ke__in=param_praktikum)
            if (param_institusi and param_tema):
                param_institusi = param_institusi.split(',')
                param_tema = param_tema.split(',')
                queryset = queryset.filter(institusi__nama__in=param_institusi).filter(tema__nama__in=param_tema)
            else:
                if (param_institusi is not None):
                    param_institusi = param_institusi.split(',')
                    queryset = queryset.filter(institusi__nama__in=param_institusi)
                if (param_tema is not None):
                    param_tema = param_tema.split(',')
                    queryset = queryset.filter(tema__nama__in=param_tema)

            # Find lembaga by Name
            # by performing substring checking
            if param_nama:
                tmp_queryset = queryset
                queryset = []
                for i in tmp_queryset:
                    if param_nama.lower() in i.nama.lower():
                        queryset.append(i)

            return queryset

        # Kasus Error Jika Parameter, Variable, dan Data tidak di set saat melakukan query
        except (ValueError, RuntimeError, TypeError, NameError):
            return {"status": "Harap isi kriteria pencarian"}


class InstitusiView(viewsets.ModelViewSet):
    """
    Provides a get method handler.
    """
    permission_classes = (AllowAny, )
    queryset = Institusi.objects.all()
    serializer_class = InstitusiSerializer


class TemaView(viewsets.ModelViewSet):
    """
    Provides a get method handler.
    """
    permission_classes = (AllowAny, )
    queryset = Tema.objects.all()
    serializer_class = TemaSerializer
