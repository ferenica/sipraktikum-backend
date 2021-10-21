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
    LaporanAkhirPraktikum
)
from laporan_praktikum.serializers import (

    KelolaLaporanPraktikumSerializer,
    KelolaLaporanPraktikumDefaultSerializer,
    LaporanAkhirPraktikumSerializer,
    LaporanAkhirPraktikumSerializer_v2,
    LaporanBorangPraktikumSerializer,
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


class UserSupervisorLembagaDetailLaporanAkhirMahasiswaView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, username):

        try:
            profile = SupervisorLembaga.objects.get(user=request.user)
            user_mahasiswa = User.objects.get(username=username)
            mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa, supervisor_lembaga=profile)

            praktikum = MahasiswaPraktikum.objects.get(mahasiswa=mahasiswa, status=True)

            laporan_akhir = LaporanAkhirPraktikum.objects.filter(mahasiswa=mahasiswa, jenis_praktikum=praktikum.list_praktikum)
            user_serializer = SupervisorLembagaSerializer(profile, context={'request': request})
            mahasiswa_serializer = MahasiswaSerializer(mahasiswa, context={'request': request})
            praktikum_serializer = PraktikumSerializer(praktikum.list_praktikum, context={'request': request})
            laporan_akhir_serializer = LaporanAkhirPraktikumSerializer_v2(laporan_akhir, context={'request': request}, many=True)

            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'List laporan akhir mahasiswa fetched successfully',
                'praktikum': praktikum_serializer.data,
                'mahasiswa': mahasiswa_serializer.data,
                'data': laporan_akhir_serializer.data,
                'user': user_serializer.data
            }

        except SupervisorLembaga.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Can not find any user data for Supervisor Lembaga'
            }

        except Mahasiswa.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Can not find any user data for Mahasiswa'
            }

        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Can not find any user data for User'
            }

        return Response(response, status=status_code)


class UserSupervisorLembagaNilaiPraktikumMahasiswaView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def update(self, request, username, id):
        try:
            skor = float(request.data.get("skor"))
            if skor >= 0 and skor <= 100:
                profile = SupervisorLembaga.objects.get(user=request.user)
                user_mahasiswa = User.objects.get(username=username)
                mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa, supervisor_lembaga=profile)
                laporan = LaporanAkhirPraktikum.objects.get(pk=id, mahasiswa=mahasiswa)

                laporan.waktu_nilai_supv_lembaga = datetime.now()
                laporan.skor_laporan_lembaga = skor
                laporan.save()

                status_code = status.HTTP_200_OK
                response = {
                    response_field[0]: 'True',
                    response_field[1]: status_code,
                    response_field[2]: 'Score updated successfully',
                }
            else:
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                response = {
                    response_field[0]: 'False',
                    response_field[1]: status_code,
                    response_field[2]: 'Please enter a valid skor input between 1-100',
                }
        except ValueError:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Please enter a valid float skor input',
            }
        except TypeError:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Please enter a valid data input',
            }
        except LaporanAkhirPraktikum.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Can not find user data for Supervisor Lembaga'
            }
        except KelolaLaporanPraktikum.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Can not find any laporan for Mahasiswa'
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Can not find any user data for User'
            }
        return Response(response, status=status_code)
