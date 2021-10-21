from rest_framework import viewsets, views
from laporan_praktikum.serializers import MahasiswaDetailPraktikumSerializerTemp
from authentication.models import (
    User,
    Mahasiswa,
    SupervisorLembaga,
    SupervisorSekolah,
    KoordinatorKuliah,
    Administrator,
    Periode
)
from authentication.serializers import (
    MahasiswaSerializer,
    SupervisorLembagaSerializer,
    SupervisorSekolahSerializer,
    KoordinatorKuliahSerializer,
    AdministratorSerializer
)
from authentication.role import Role
from lembaga.models import (
    Lembaga
)

from laporan_praktikum.models import (
    Praktikum,
    KelolaLaporanPraktikum,
    LaporanBorangPraktikum,
    LaporanAkhirPraktikum,
    MahasiswaPraktikum,
    Praktikum,
    LaporanAkhirPraktikum,
    TemplateBorangPenilaianPraktikum
)

from laporan_praktikum.serializers import (

    KelolaLaporanPraktikumSerializer,
    KelolaLaporanPraktikumDefaultSerializer,
    LaporanAkhirPraktikumSerializer,
    LaporanAkhirPraktikumSerializer_v2,
    LaporanBorangPraktikumSerializer,
    TemplateLaporanBorangPraktikumSerializer_v2,
    MahasiswaDetailPraktikumSerializer,
    SupervisorSekolahListMahasiswaSerializer,
    SupervisorLembagaListMahasiswaSerializer,
    SupervisorLembagaSpesificSerializer,
    RiwayatLaporanPraktikumMahasiswaSerializer,
    PraktikumSerializer,
    KoordinatorKuliahListMahasiswaSerializer,
    AdministratorListUserSerializer,

)
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError

from django.core import serializers
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound


import json
import datetime
from dateutil.parser import parse
from datetime import datetime

response_field = ['success', 'status_code', 'message']

STR_ERROR_MESSAGE_SOMETHING = "Something's wrong, try again..."
STR_CANNOT_FIND_USER_DATA_FOR_SUPERVISOR_SEKOLAH = 'Can not find user data for Supervisor Sekolah'


@api_view(["GET"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_template_laporan_borang(request):
    '''
    Fungsi untuk get hasil upload Template Laporan Borang for SupervisorSekolah
    '''
    try:
        supervisor_sekolah = SupervisorSekolah.objects.get(user=request.user)
        laporan_template_borang = TemplateBorangPenilaianPraktikum.objects.get(supervisor_sekolah=supervisor_sekolah)
        serializer_template_borang = TemplateLaporanBorangPraktikumSerializer_v2(laporan_template_borang, context={'request': request})

        status_code = status.HTTP_200_OK
        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: 'Template Borang fetched successfully',
            'data': serializer_template_borang.data
        }

    except SupervisorSekolah.DoesNotExist:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: STR_CANNOT_FIND_USER_DATA_FOR_SUPERVISOR_SEKOLAH,
        }
    except TemplateBorangPenilaianPraktikum.DoesNotExist:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Can not find data for Template Borang Penilaian Praktikum',
        }
    return Response(response, status=status_code)


@ api_view(["PUT", "POST"])
@ authentication_classes([JSONWebTokenAuthentication])
@ permission_classes([IsAuthenticated])
def crud_template_laporan_borang(request):
    '''
    Fungsi untuk Upload Template Laporan Borang dan share ke seluruh Mahasiswa yang di supervisinya
    '''
    try:
        supervisor_sekolah = SupervisorSekolah.objects.get(user=request.user)
        file_t_borang_supv_sekolah = request.data['template_borang_supv_sekolah']
        file_t_borang_supv_lembaga = request.data['template_borang_supv_lembaga']
        file_t_borang_supv_perkuliahan = request.data['template_borang_supv_perkuliahan']
        obj, created = TemplateBorangPenilaianPraktikum.objects.update_or_create(
            supervisor_sekolah=supervisor_sekolah,
            defaults={'t_borang_supv_sekolah': file_t_borang_supv_sekolah,
                      't_borang_supv_lembaga': file_t_borang_supv_lembaga,
                      't_borang_supv_perkuliahan': file_t_borang_supv_perkuliahan
                      }
        )
        status_code = status.HTTP_201_CREATED
        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: 'Template Borang uploaded successfully'
        }

    except AttributeError:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: STR_ERROR_MESSAGE_SOMETHING,
        }

    except KeyError:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: STR_ERROR_MESSAGE_SOMETHING,
        }

    except ValueError:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: STR_ERROR_MESSAGE_SOMETHING,
        }

    except SupervisorSekolah.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: STR_CANNOT_FIND_USER_DATA_FOR_SUPERVISOR_SEKOLAH,
        }
    return Response(response, status=status_code)
