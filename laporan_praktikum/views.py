from rest_framework import viewsets, views
from .serializers import MahasiswaDetailPraktikumSerializerTemp
from authentication.models import (
    User,
    Mahasiswa,
    SupervisorLembaga,
    SupervisorSekolah,
    KoordinatorKuliah,
    Administrator,
    Periode,
    Config
)
from authentication.serializers import (
    MahasiswaSerializer,
    SupervisorLembagaSerializer,
    SupervisorSekolahSerializer,
    KoordinatorKuliahSerializer,
    AdministratorSerializer,
    ConfigSerializer
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
    MahasiswaWithJenisPraktikumSerializer,
    KelolaLaporanPraktikumSerializer,
    KelolaLaporanPraktikumDefaultSerializer,
    LaporanAkhirPraktikumSerializer,
    LaporanAkhirPraktikumSerializer_v2,
    LaporanBorangPraktikumSerializer,
    MahasiswaDetailPraktikumSerializer,
    SupervisorSekolahListMahasiswaSerializer,
    SupervisorLembagaListMahasiswaSerializer,
    SupervisorLembagaSpesificSerializer,
    SupervisorLembagaUsernameSerializer,
    RiwayatLaporanPraktikumMahasiswaSerializer,
    PraktikumSerializer,
    KoordinatorKuliahListMahasiswaSerializer,
    AdministratorListUserSerializer,
    TemplateLaporanBorangPraktikumSerializer_v2
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

import base64
from django.core.files.base import ContentFile

STR_ERROR_MESSAGE_SOMETHING = 'Something\'s wrong, try again...'


def parse_time_custom(datetime_inp):
    '''
    CUSTOM PARSER FOR TIME DD-MM-YY hh:mm
    '''
    return datetime.strptime(datetime_inp, '%d-%m-%Y %H:%M')


response_field = ['success', 'status_code', 'message']
error_message_404_supervisor_sekolah = 'Can not find user data for Supervisor Sekolah'
error_message_404_koordinator_kuliah = 'Can not find user data for Koordinator Praktikum'
error_message_404_administrator = 'Can not find user data for Administrator'
error_message_404_mahasiswa = 'Can not find user data for Mahasiswa'
error_message_404_supervisor_lembaga = 'Can not find user data for Supervisor Lembaga'
error_message_404_user = 'Can not find user data for User'
error_message_404_praktikum = 'Can not find any praktikum data for mahasiswa'
error_message_404_laporan = 'Can not find any laporan data for mahasiswa'
error_message_404_lembaga = 'Can not find lembaga'


class UserSupervisorSekolahListMahasiswaView(RetrieveAPIView):  # pragma: no cover
    '''''''''''''''''''''''''''
    Supervisor Sekolah Related
    '''''''''''''''''''''''''''
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):

        try:
            profile = SupervisorSekolah.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            serializer = SupervisorSekolahListMahasiswaSerializer(profile, context={'request': request})
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'List mahasiswa fetch successfully',
                'data': serializer.data
            }
        except SupervisorSekolah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_supervisor_sekolah
            }
        return Response(response, status=status_code)


class UserMahasiswaListPraktikumView(RetrieveAPIView):  # pragma: no cover
    '''''''''''''''''''''
    User Mahasiswa Related
    '''''''''''''''''''''
    permission_classes = (IsAuthenticated, )
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            profile = Mahasiswa.objects.get(user=request.user)
            user = MahasiswaPraktikum.objects.filter(mahasiswa=profile)
            status_code = status.HTTP_200_OK
            serializer = MahasiswaDetailPraktikumSerializer(user, context={'request': request}, many=True)
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Jenis praktikum fetched successfully',
                'data': serializer.data
            }

        except Mahasiswa.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Can not find user data for Mahasiswa'
            }
        return Response(response, status=status_code)


@api_view(["GET"])  # pragma: no cover
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_list_laporan_praktikum_detail(request):
    try:
        mahasiswa = Mahasiswa.objects.get(user=request.user)
        supervisor_sekolah = mahasiswa.supervisor_sekolah

        praktikum = MahasiswaPraktikum.objects.get(mahasiswa=mahasiswa, status=True)
        laporan_mingguan = KelolaLaporanPraktikum.objects.filter(mahasiswa=mahasiswa, jenis_praktikum=praktikum.list_praktikum)
        laporan_akhir = LaporanAkhirPraktikum.objects.filter(mahasiswa=mahasiswa, jenis_praktikum=praktikum.list_praktikum)
        laporan_borang = LaporanBorangPraktikum.objects.filter(mahasiswa=mahasiswa, jenis_praktikum=praktikum.list_praktikum)
        template_laporan_borang = TemplateBorangPenilaianPraktikum.objects.get(supervisor_sekolah=supervisor_sekolah)

        serializer_mahasiswa = MahasiswaSerializer(mahasiswa, context={'request': request})
        serializer_laporan_mingguan = KelolaLaporanPraktikumSerializer(laporan_mingguan,
                                            context={'request': request}, many=True)
        serializer_laporan_akhir = LaporanAkhirPraktikumSerializer_v2(laporan_akhir,
                                            context={'request': request}, many=True)

        serializer_laporan_borang = LaporanBorangPraktikumSerializer(laporan_borang,
                                            context={'request': request}, many=True)

        serializer_template_laporan = TemplateLaporanBorangPraktikumSerializer_v2(template_laporan_borang,
                                context={'request': request})

        status_code = status.HTTP_200_OK

        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: 'Jenis praktikum fetched successfully',
            'profile': serializer_mahasiswa.data,
            'laporan_mingguan': serializer_laporan_mingguan.data,
            'laporan_akhir': serializer_laporan_akhir.data,
            'laporan_borang': serializer_laporan_borang.data,
            'template_borang': serializer_template_laporan.data
        }

    except Mahasiswa.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Can not find user data for Mahasiswa'
        }

    except MahasiswaPraktikum.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: error_message_404_praktikum
        }

    except TemplateBorangPenilaianPraktikum.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: "Your Supervisor Sekolah hasn't been uploaded the Template Borang"
        }
    return Response(response, status=status_code)


@api_view(["GET"])  # pragma: no cover
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_laporan_mahasiswa_by_id(request, id):
    # Laporan mahasiswa by id
    profile = Mahasiswa.objects.get(user=request.user)
    laporan_mahasiswa = KelolaLaporanPraktikum.objects.filter(Q(mahasiswa=profile) & Q(id=id))
    serializer_mahasiswa = MahasiswaSerializer(profile, context={'request': request})
    serializer_laporan = RiwayatLaporanPraktikumMahasiswaSerializer(laporan_mahasiswa, context={'request': request}, many=True)
    status_code = status.HTTP_200_OK
    response = {
        response_field[0]: 'True',
        response_field[1]: status_code,
        response_field[2]: 'Laporan Praktikum fetched successfully',
        'profile': serializer_mahasiswa.data,
        'data': serializer_laporan.data
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])  # pragma: no cover
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_laporan_akhir_mahasiswa_by_id(request, id):
    # Laporan mahasiswa by id
    profile = Mahasiswa.objects.get(user=request.user)
    laporan_akhir_mahasiswa = LaporanAkhirPraktikum.objects.filter(Q(mahasiswa=profile) & Q(id=id))
    serializer_mahasiswa = MahasiswaSerializer(profile, context={'request': request})
    serializer_laporan = LaporanAkhirPraktikumSerializer_v2(laporan_akhir_mahasiswa,
                        context={'request': request}, many=True)
    status_code = status.HTTP_200_OK
    response = {
        response_field[0]: 'True',
        response_field[1]: status_code,
        response_field[2]: 'Laporan Praktikum fetched successfully',
        'profile': serializer_mahasiswa.data,
        'data': serializer_laporan.data
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])  # pragma: no cover
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_laporan_borang_mahasiswa_by_id(request, id):
    # Laporan mahasiswa by id

    try:
        profile = Mahasiswa.objects.get(user=request.user)
        laporan_borang_mahasiswa = LaporanBorangPraktikum.objects.filter(Q(mahasiswa=profile) & Q(id=id))
        serializer_mahasiswa = MahasiswaSerializer(profile, context={'request': request})
        serializer_laporan = LaporanBorangPraktikumSerializer(laporan_borang_mahasiswa,
                            context={'request': request}, many=True)

        # Get supervisor_sekolah value from rows
        supervisor_sekolah = profile.supervisor_sekolah

        template_laporan_borang = TemplateBorangPenilaianPraktikum.objects.get(supervisor_sekolah=supervisor_sekolah)
        serializer_template_laporan = TemplateLaporanBorangPraktikumSerializer_v2(template_laporan_borang,
                                        context={'request': request})
        status_code = status.HTTP_200_OK
        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: 'Laporan Praktikum fetched successfully',
            'profile': serializer_mahasiswa.data,
            'data': serializer_laporan.data,
            'template_borang': serializer_template_laporan.data
        }

    except Mahasiswa.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Can not find user data for Mahasiswa'
        }

    except SupervisorSekolah.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: error_message_404_supervisor_sekolah
        }
    return Response(response, status=status_code)


class UserSupervisorLembagaListMahasiswaView(RetrieveAPIView):  # pragma: no cover
    '''''''''''''''''''''
    Supervisor Lembaga Mahasiswa Related
    '''''''''''''''''''''
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            profile = SupervisorLembaga.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            serializer = SupervisorLembagaListMahasiswaSerializer(profile, context={'request': request})

            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'List mahasiswa fetch successfully',
                'data': serializer.data
            }
        except SupervisorLembaga.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Can not find user data for Supervisor Lembaga'
            }
        return Response(response, status=status_code)


@api_view(["GET", "PUT", "POST"])  # pragma: no cover
@permission_classes([AllowAny])
def get_supervisor_lembaga_by_id_lembaga(request, id_lembaga):
    try:
        nama_lembaga = Lembaga.objects.get(id=id_lembaga)
        supervisor_lembaga = SupervisorLembaga.objects.filter(lembaga=nama_lembaga)
        if supervisor_lembaga.count() == 0:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Can not find Supervisor Lembaga'
            }
            return Response(response, status=status_code)

        serializer = SupervisorLembagaSpesificSerializer(supervisor_lembaga, context={'request': request}, many=True)
        status_code = status.HTTP_200_OK
        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: 'Supervisor Lembaga fetched successfully',
            'data': serializer.data
        }

    except Lembaga.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: error_message_404_lembaga
        }

    return Response(response, status=status_code)


@api_view(["GET", "PUT"])  # pragma: no cover
@permission_classes([AllowAny])
def get_supervisor_lembaga_by_username(request, username):
    try:
        supervisor_lembaga = User.objects.get(username=username)
        serializer = SupervisorLembagaUsernameSerializer(supervisor_lembaga, context={'request': request}, many=False)
        status_code = status.HTTP_200_OK
        response = serializer.data

    except User.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Can not find Supervisor Lembaga'
        }

    return Response(response, status=status_code)


@api_view(["GET", "PUT", "POST", "DELETE"])  # pragma: no cover
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_or_update_laporan_praktikum(request, username):
    try:
        profile_supervisor_sekolah = SupervisorSekolah.objects.get(user=request.user)
        user_mahasiswa = User.objects.get(username=username)
        mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa, supervisor_sekolah=profile_supervisor_sekolah)
        praktikum = MahasiswaPraktikum.objects.get(mahasiswa=mahasiswa, status=True)
        laporan_mingguan = KelolaLaporanPraktikum.objects.filter(mahasiswa=mahasiswa,
                            jenis_praktikum=praktikum.list_praktikum).order_by('nama_laporan')
        laporan_akhir = LaporanAkhirPraktikum.objects.filter(mahasiswa=mahasiswa, jenis_praktikum=praktikum.list_praktikum)
        laporan_borang = LaporanBorangPraktikum.objects.filter(mahasiswa=mahasiswa, jenis_praktikum=praktikum.list_praktikum)

        if request.method == "GET":
            serializer_mahasiswa = MahasiswaSerializer(mahasiswa, context={'request': request})
            serializer_laporan_mingguan = KelolaLaporanPraktikumSerializer(laporan_mingguan,
                                            context={'request': request}, many=True)
            serializer_laporan_akhir = LaporanAkhirPraktikumSerializer_v2(laporan_akhir,
                                            context={'request': request}, many=True)

            serializer_laporan_borang = LaporanBorangPraktikumSerializer(laporan_borang,
                                            context={'request': request}, many=True)

            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'List mahasiswa fetch successfully',
                'profile': serializer_mahasiswa.data,
                'laporan_mingguan': serializer_laporan_mingguan.data,
                'laporan_akhir': serializer_laporan_akhir.data,
                'laporan_borang': serializer_laporan_borang.data,
            }
            return Response(response, status=status.HTTP_200_OK)

        elif request.method == "POST" or request.method == "PUT":
            '''
            Docs API
            {
                "username_mahasiswa": "username_mahasiswa",
                "username_supervisor_lembaga": "username_supervisor",
                "laporan_mingguan": [],
                "laporan_akhir": [],
                "laporan_borang":[]
            }
            '''

            username_supervisor_lembaga = request.data['username_supervisor_lembaga']

            data_lap_mingguan = list(request.data['laporan_mingguan'])
            data_lap_akhir = list(request.data['laporan_akhir'])
            data_lap_borang = list(request.data['laporan_borang'])

            # check supervisor_lembaga available or not
            if mahasiswa.supervisor_lembaga is None:
                profile_supervisor_lembaga = User.objects.get(username=username_supervisor_lembaga)
                supervisor_lembaga = SupervisorLembaga.objects.get(user=profile_supervisor_lembaga)
                mahasiswa.supervisor_lembaga = supervisor_lembaga

            if data_lap_mingguan:
                for attribute in data_lap_mingguan:
                    laporan_praktikum = Praktikum.objects.get(jenis_praktikum=attribute['jenis_praktikum'])
                    if attribute["waktu_deadline"] is not None:
                        waktu_deadline = parse_time_custom(attribute["waktu_deadline"])
                    obj, created = KelolaLaporanPraktikum.objects.update_or_create(
                        mahasiswa=mahasiswa,
                        jenis_praktikum=laporan_praktikum,
                        nama_laporan=attribute["nama_laporan"],
                        defaults={'waktu_deadline': waktu_deadline,
                        'status_publikasi': attribute["status_publikasi"]
                                  }
                    )

            if data_lap_akhir:
                for attribute in data_lap_akhir:
                    laporan_praktikum = Praktikum.objects.get(jenis_praktikum=attribute['jenis_praktikum'])

                    if attribute["waktu_deadline"] is not None:
                        waktu_deadline = parse_time_custom(attribute["waktu_deadline"])
                    obj, created = LaporanAkhirPraktikum.objects.update_or_create(
                        mahasiswa=mahasiswa,
                        jenis_praktikum=laporan_praktikum,
                        nama_laporan=attribute["nama_laporan"],
                        defaults={'waktu_deadline': waktu_deadline,
                        'status_publikasi': attribute["status_publikasi"]
                                  }
                    )

            if data_lap_borang:
                for attribute in data_lap_borang:
                    laporan_praktikum = Praktikum.objects.get(jenis_praktikum=attribute['jenis_praktikum'])
                    if attribute["waktu_deadline"] is not None:
                        waktu_deadline = parse_time_custom(attribute["waktu_deadline"])
                    obj, created = LaporanBorangPraktikum.objects.update_or_create(
                        mahasiswa=mahasiswa,
                        jenis_praktikum=laporan_praktikum,
                        nama_laporan=attribute["nama_laporan"],
                        defaults={'waktu_deadline': waktu_deadline,
                        'status_publikasi': attribute["status_publikasi"]
                                  }
                    )

            status_code = status.HTTP_201_CREATED
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Laporan Praktikum successfully update',
            }

    except User.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: error_message_404_user
        }

    except Mahasiswa.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: error_message_404_user
        }

    except Praktikum.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: error_message_404_praktikum
        }

    except MahasiswaPraktikum.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: error_message_404_praktikum
        }
    return Response(response, status=status_code)


@api_view(["DELETE"])  # pragma: no cover
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_laporan_praktikum(request, username, tipe, pk):
    status_code = status.HTTP_200_OK
    response = {
        response_field[0]: 'True',
        response_field[1]: status_code,
        response_field[2]: "Laporan successfully deleted"
    }

    if tipe == 'mingguan':
        KelolaLaporanPraktikum.objects.get(pk=pk).delete()

    elif tipe == 'borang':
        LaporanBorangPraktikum.objects.get(pk=pk).delete()

    elif tipe == 'akhir':
        LaporanAkhirPraktikum.objects.get(pk=pk).delete()

    return Response(response, status=status_code)


@api_view(["PUT", "POST"])  # pragma: no cover
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def submit_link_laporan_praktikum(request):
    try:
        profile = Mahasiswa.objects.get(user=request.user)
        id_laporan = request.data['id']
        check_laporan_ownership = (profile == KelolaLaporanPraktikum.objects.get(id=id_laporan).mahasiswa)

        if not check_laporan_ownership:
            response = {
                response_field[0]: 'True',
                response_field[1]: status.HTTP_403_FORBIDDEN,
                response_field[2]: 'Forbidden access to laporan praktikum',
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        if request.data['link_submisi'][:11].lower() == "javascript:":
            response = {
                response_field[0]: 'True',
                response_field[1]: status.HTTP_403_FORBIDDEN,
                response_field[2]: 'Forbidden protocol for the link',
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        # Update link submit laporan praktikum mahasiswa and waktu_submisi (minus 5 hour to localzone)
        KelolaLaporanPraktikum.objects.filter(id=id_laporan).update(
            waktu_submisi=parse_time_custom(request.data['waktu_submisi']),
            link_submisi=request.data['link_submisi'],
            status_submisi=request.data['status_submisi']
        )

        status_code = status.HTTP_201_CREATED
        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: 'Link laporan praktikum successfully update',
        }
        return Response(response, status=status_code)

    except Mahasiswa.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Can not find user data for Mahasiswa',
        }
        return Response(response, status=status_code)

    except KelolaLaporanPraktikum.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Can not find the laporan with the specific id',
        }
        return Response(response, status=status_code)


@api_view(["GET", "PUT", "POST"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def crud_submisi_laporan_akhir_mahasiswa(request):
    try:
        mahasiswa = Mahasiswa.objects.get(user=request.user)
        if request.method == "POST" or request.method == "PUT":
            nama_laporan = request.data["nama_laporan"]
            nama_lembaga = Lembaga.objects.get(nama=request.data['nama_lembaga'])
            jenis_praktikum = Praktikum.objects.get(jenis_praktikum=request.data['jenis_praktikum'])
            periode_praktikum = request.data['periode_praktikum']
            waktu_submisi = parse_time_custom(request.data['waktu_submisi'])
            status_submisi = request.data['status_submisi']
            file_laporan_akhir = request.data.get('file_laporan_akhir')
            file_profil_lembaga = request.data.get('file_profil_lembaga')

            if status_submisi.lower() == "true" or status_submisi is True:
                status_submisi = True

            else:
                status_submisi = False

            obj, created = LaporanAkhirPraktikum.objects.update_or_create(
                mahasiswa=mahasiswa,
                nama_laporan=nama_laporan,
                jenis_praktikum=jenis_praktikum,
                defaults={'lembaga': nama_lembaga, 'waktu_submisi': waktu_submisi,
                          'status_submisi': status_submisi,
                          'periode_praktikum': periode_praktikum,
                          'laporan_akhir': file_laporan_akhir,
                          'profil_lembaga': file_profil_lembaga
                          }
            )
            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Laporan akhir submitted successfully',
            }

    except Mahasiswa.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Can not find user data for Mahasiswa',
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
    return Response(response, status=status_code)


@api_view(["GET", "PUT", "POST"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def crud_submisi_laporan_borang_mahasiswa(request):
    try:
        mahasiswa = Mahasiswa.objects.get(user=request.user)
        if request.method == "POST" or request.method == "PUT":
            nama_laporan = request.data["nama_laporan"]
            jenis_praktikum = Praktikum.objects.get(jenis_praktikum=request.data['jenis_praktikum'])
            waktu_submisi = parse_time_custom(request.data['waktu_submisi'])
            status_submisi = request.data['status_submisi']
            file_borang_supv_lembaga = request.data.get('file_borang_supv_lembaga')
            file_borang_supv_sekolah = request.data.get('file_borang_supv_sekolah')
            file_borang_penilaian_kuliah = request.data.get('file_borang_penilaian_kuliah')

            if status_submisi.lower() == "true" or status_submisi is True:
                status_submisi = True

            else:
                status_submisi = False

            obj, created = LaporanBorangPraktikum.objects.update_or_create(
                mahasiswa=mahasiswa,
                nama_laporan=nama_laporan,
                jenis_praktikum=jenis_praktikum,
                defaults={'waktu_submisi': waktu_submisi,
                          'status_submisi': status_submisi,
                          'borang_supv_sekolah': file_borang_supv_sekolah,
                          'borang_supv_lembaga': file_borang_supv_lembaga,
                          'borang_supv_perkuliahan': file_borang_penilaian_kuliah
                          }
            )

            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Laporan akhir submitted successfully',
            }

    except Mahasiswa.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Can not find user data for Mahasiswa',
        }

    except LaporanBorangPraktikum.DoesNotExist:
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Can not find Laporan Borang Praktikum',
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
    return Response(response, status=status_code)


class UserSupervisorSekolahListPraktikumMahasiswaView(RetrieveAPIView):  # pragma: no cover
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, username):
        try:
            profile = SupervisorSekolah.objects.get(user=request.user)
            user_mahasiswa = User.objects.get(username=username)
            mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa, supervisor_sekolah=profile)
            praktikum = MahasiswaPraktikum.objects.get(mahasiswa=mahasiswa, status=True)

            laporan_mingguan = KelolaLaporanPraktikum.objects.filter(mahasiswa=mahasiswa, jenis_praktikum=praktikum.list_praktikum)
            laporan_akhir = LaporanAkhirPraktikum.objects.filter(mahasiswa=mahasiswa, jenis_praktikum=praktikum.list_praktikum)
            laporan_borang = LaporanBorangPraktikum.objects.filter(mahasiswa=mahasiswa, jenis_praktikum=praktikum.list_praktikum)

            praktikum_serializer = PraktikumSerializer(praktikum.list_praktikum, context={'request': request})
            mahasiswa_serializer = MahasiswaSerializer(mahasiswa, context={'request': request})
            user_serializer = SupervisorSekolahSerializer(profile, context={'request': request})

            serializer_laporan_mingguan = KelolaLaporanPraktikumSerializer(laporan_mingguan,
                                                context={'request': request}, many=True)
            serializer_laporan_akhir = LaporanAkhirPraktikumSerializer_v2(laporan_akhir,
                                                context={'request': request}, many=True)
            serializer_laporan_borang = LaporanBorangPraktikumSerializer(laporan_borang,
                                                context={'request': request}, many=True)

            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'List praktikum mahasiswa fetch successfully',
                'laporan_mingguan': serializer_laporan_mingguan.data,
                'laporan_akhir': serializer_laporan_akhir.data,
                'laporan_borang': serializer_laporan_borang.data,
                'praktikum': praktikum_serializer.data,
                'mahasiswa': mahasiswa_serializer.data,
                'user': user_serializer.data
            }
        except SupervisorSekolah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_supervisor_sekolah
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        except MahasiswaPraktikum.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_praktikum
            }
        return Response(response, status=status_code)


class UserSupervisorSekolahDetailLaporanMingguanMahasiswaView(RetrieveAPIView):
    """
    Return detail laporan mingguan data of mahasiswa of supervisor sekolah
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, username, id):
        try:
            profile = SupervisorSekolah.objects.get(user=request.user)
            user_mahasiswa = User.objects.get(username=username)
            mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa, supervisor_sekolah=profile)
            laporan = KelolaLaporanPraktikum.objects.get(pk=id, mahasiswa=mahasiswa)

            mahasiswa_serializer = MahasiswaSerializer(mahasiswa, context={'request': request})
            user_serializer = SupervisorSekolahSerializer(profile, context={'request': request})
            laporan_serializer = KelolaLaporanPraktikumSerializer(laporan, context={'request': request})
            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Detail praktikum mahasiswa fetch successfully',
                'data': laporan_serializer.data,
                'user': user_serializer.data,
                'mahasiswa': mahasiswa_serializer.data
            }
        except SupervisorSekolah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_supervisor_sekolah
            }
        except KelolaLaporanPraktikum.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_laporan
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        return Response(response, status=status_code)


class UserSupervisorSekolahDetailLaporanAkhirMahasiswaView(RetrieveAPIView):
    """
    Return detail laporan akhir data of mahasiswa of supervisor sekolah
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, username, id):
        try:
            profile = SupervisorSekolah.objects.get(user=request.user)
            user_mahasiswa = User.objects.get(username=username)
            mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa, supervisor_sekolah=profile)
            laporan = LaporanAkhirPraktikum.objects.get(pk=id, mahasiswa=mahasiswa)

            mahasiswa_serializer = MahasiswaSerializer(mahasiswa, context={'request': request})
            user_serializer = SupervisorSekolahSerializer(profile, context={'request': request})
            laporan_serializer = LaporanAkhirPraktikumSerializer_v2(laporan, context={'request': request})
            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Detail laporan akhir mahasiswa fetch successfully',
                'data': laporan_serializer.data,
                'user': user_serializer.data,
                'mahasiswa': mahasiswa_serializer.data
            }
        except SupervisorSekolah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_supervisor_sekolah
            }
        except LaporanAkhirPraktikum.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_laporan
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        return Response(response, status=status_code)


class UserSupervisorSekolahDetailBorangMahasiswaView(RetrieveAPIView):
    """
    Return detail borang data of mahasiswa of supervisor sekolah
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, username, id):
        try:
            profile = SupervisorSekolah.objects.get(user=request.user)
            user_mahasiswa = User.objects.get(username=username)
            mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa, supervisor_sekolah=profile)
            laporan = LaporanBorangPraktikum.objects.get(pk=id, mahasiswa=mahasiswa)

            mahasiswa_serializer = MahasiswaSerializer(mahasiswa, context={'request': request})
            user_serializer = SupervisorSekolahSerializer(profile, context={'request': request})
            laporan_serializer = LaporanBorangPraktikumSerializer(laporan, context={'request': request})
            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Detail laporan akhir mahasiswa fetch successfully',
                'data': laporan_serializer.data,
                'user': user_serializer.data,
                'mahasiswa': mahasiswa_serializer.data
            }
        except SupervisorSekolah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_supervisor_sekolah
            }
        except LaporanBorangPraktikum.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_laporan
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        return Response(response, status=status_code)


class UserSupervisorSekolahNilaiLaporanMingguanMahasiswaView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def update(self, request, username, id):
        try:
            skor = float(request.data.get("skor"))
            if skor >= 0 and skor <= 100:
                profile = SupervisorSekolah.objects.get(user=request.user)
                user_mahasiswa = User.objects.get(username=username)
                mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa, supervisor_sekolah=profile)
                laporan = KelolaLaporanPraktikum.objects.get(pk=id, mahasiswa=mahasiswa)

                laporan.waktu_nilai_supv_sekolah = datetime.now()
                laporan.skor_laporan_sekolah = skor
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
        except SupervisorSekolah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_supervisor_sekolah
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
                response_field[2]: 'Can not find any user data for Mahasiswa'
            }
        return Response(response, status=status_code)


class UserSupervisorSekolahNilaiLaporanAkhirMahasiswaView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def update(self, request, username, id):
        try:
            skor = float(request.data.get("skor"))
            feedback = request.data.get("feedback")
            if skor >= 0 and skor <= 100:
                profile = SupervisorSekolah.objects.get(user=request.user)
                user_mahasiswa = User.objects.get(username=username)
                mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa, supervisor_sekolah=profile)
                laporan = LaporanAkhirPraktikum.objects.get(pk=id, mahasiswa=mahasiswa)

                laporan.waktu_nilai_supv_sekolah = datetime.now()
                laporan.skor_laporan_sekolah = skor
                laporan.umpan_balik = feedback
                laporan.save()

                status_code = status.HTTP_200_OK
                response = {
                    response_field[0]: 'True',
                    response_field[1]: status_code,
                    response_field[2]: 'Data updated successfully',
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
        except SupervisorSekolah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_supervisor_sekolah
            }
        except LaporanAkhirPraktikum.DoesNotExist:
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
                response_field[2]: 'Can not find any user data for Mahasiswa'
            }
        return Response(response, status=status_code)


class UserKoordinatorKuliahListMahasiswaView(RetrieveAPIView):  # pragma: no cover

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            profile = KoordinatorKuliah.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            serializer = KoordinatorKuliahListMahasiswaSerializer(profile, context={'request': request})
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'List mahasiswa fetch successfully',
                'data': serializer.data
            }
        except KoordinatorKuliah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_koordinator_kuliah
            }
        return Response(response, status=status_code)


class UserAdministratorListUserView(RetrieveAPIView):  # pragma: no cover

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            profile = Administrator.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            serializer = AdministratorListUserSerializer(profile, context={'request': request})
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'List users fetch successfully',
                'data': serializer.data
            }
        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_administrator
            }
        return Response(response, status=status_code)


class UserKoordinatorKuliahListPraktikumMahasiswaView(RetrieveAPIView):  # pragma: no cover
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, username):
        try:
            profile = KoordinatorKuliah.objects.get(user=request.user)
            user_mahasiswa = User.objects.get(username=username)
            mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa)
            praktikum = MahasiswaPraktikum.objects.get(mahasiswa=mahasiswa, status=True)

            laporan_mingguan = KelolaLaporanPraktikum.objects.filter(mahasiswa=mahasiswa, jenis_praktikum=praktikum.list_praktikum)
            laporan_akhir = LaporanAkhirPraktikum.objects.filter(mahasiswa=mahasiswa, jenis_praktikum=praktikum.list_praktikum)
            laporan_borang = LaporanBorangPraktikum.objects.filter(mahasiswa=mahasiswa, jenis_praktikum=praktikum.list_praktikum)

            praktikum_serializer = PraktikumSerializer(praktikum.list_praktikum, context={'request': request})
            mahasiswa_serializer = MahasiswaSerializer(mahasiswa, context={'request': request})
            user_serializer = SupervisorSekolahSerializer(profile, context={'request': request})

            serializer_laporan_mingguan = KelolaLaporanPraktikumSerializer(laporan_mingguan,
                                                context={'request': request}, many=True)
            serializer_laporan_akhir = LaporanAkhirPraktikumSerializer_v2(laporan_akhir,
                                                context={'request': request}, many=True)
            serializer_laporan_borang = LaporanBorangPraktikumSerializer(laporan_borang,
                                                context={'request': request}, many=True)

            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'List praktikum mahasiswa fetch successfully',
                'laporan_mingguan': serializer_laporan_mingguan.data,
                'laporan_akhir': serializer_laporan_akhir.data,
                'laporan_borang': serializer_laporan_borang.data,
                'praktikum': praktikum_serializer.data,
                'mahasiswa': mahasiswa_serializer.data,
                'user': user_serializer.data
            }
        except KoordinatorKuliah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_koordinator_kuliah
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        except MahasiswaPraktikum.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_praktikum
            }
        return Response(response, status=status_code)


class UserKoordinatorKuliahDetailLaporanMingguanMahasiswaView(RetrieveAPIView):
    """
    Return detail laporan data of mahasiswa of koordinator kuliah
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, username, id):
        try:
            profile = KoordinatorKuliah.objects.get(user=request.user)
            user_mahasiswa = User.objects.get(username=username)
            mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa)
            laporan = KelolaLaporanPraktikum.objects.get(pk=id, mahasiswa=mahasiswa)

            mahasiswa_serializer = MahasiswaSerializer(mahasiswa, context={'request': request})
            user_serializer = KoordinatorKuliahSerializer(profile, context={'request': request})
            laporan_serializer = KelolaLaporanPraktikumSerializer(laporan, context={'request': request})
            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Detail praktikum mahasiswa fetch successfully',
                'data': laporan_serializer.data,
                'user': user_serializer.data,
                'mahasiswa': mahasiswa_serializer.data
            }
        except KoordinatorKuliah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_koordinator_kuliah
            }
        except KelolaLaporanPraktikum.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_laporan
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        return Response(response, status=status_code)


class UserKoordinatorKuliahDetailLaporanAkhirMahasiswaView(RetrieveAPIView):
    """
    Return detail laporan akhir data of mahasiswa of supervisor sekolah
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, username, id):
        try:
            profile = KoordinatorKuliah.objects.get(user=request.user)
            user_mahasiswa = User.objects.get(username=username)
            mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa)
            laporan = LaporanAkhirPraktikum.objects.get(pk=id, mahasiswa=mahasiswa)

            mahasiswa_serializer = MahasiswaSerializer(mahasiswa, context={'request': request})
            user_serializer = KoordinatorKuliahSerializer(profile, context={'request': request})
            laporan_serializer = LaporanAkhirPraktikumSerializer_v2(laporan, context={'request': request})
            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Detail laporan akhir mahasiswa fetch successfully',
                'data': laporan_serializer.data,
                'user': user_serializer.data,
                'mahasiswa': mahasiswa_serializer.data
            }
        except KoordinatorKuliah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_koordinator_kuliah
            }
        except LaporanAkhirPraktikum.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_laporan
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        return Response(response, status=status_code)


class UserKoordinatorKuliahDetailBorangMahasiswaView(RetrieveAPIView):
    """
    Return detail borang data of mahasiswa of supervisor sekolah
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, username, id):
        try:
            profile = KoordinatorKuliah.objects.get(user=request.user)
            user_mahasiswa = User.objects.get(username=username)
            mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa)
            laporan = LaporanBorangPraktikum.objects.get(pk=id, mahasiswa=mahasiswa)

            mahasiswa_serializer = MahasiswaSerializer(mahasiswa, context={'request': request})
            user_serializer = KoordinatorKuliahSerializer(profile, context={'request': request})
            laporan_serializer = LaporanBorangPraktikumSerializer(laporan, context={'request': request})
            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Detail laporan akhir mahasiswa fetch successfully',
                'data': laporan_serializer.data,
                'user': user_serializer.data,
                'mahasiswa': mahasiswa_serializer.data
            }
        except KoordinatorKuliah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_koordinator_kuliah
            }
        except LaporanBorangPraktikum.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_laporan
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        return Response(response, status=status_code)


class UserAdministratorKelolaUserDetailUserMahasiswaView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, username):
        try:
            profile = Administrator.objects.get(user=request.user)
            user_mahasiswa = User.objects.get(username=username)
            mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa)
            mahasiswa_praktikum = MahasiswaPraktikum.objects.get(status=True, mahasiswa=mahasiswa)

            mahasiswa_serializer = MahasiswaDetailPraktikumSerializer(mahasiswa_praktikum, context={'request': request})
            user_serializer = AdministratorSerializer(profile, context={'request': request})
            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Detail kelola mahasiswa fetch successfully',
                'data': mahasiswa_serializer.data,
                'user': user_serializer.data
            }
        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_administrator
            }
        except MahasiswaPraktikum.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: "Active data praktikum can't be found"
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        except Mahasiswa.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_mahasiswa
            }
        return Response(response, status=status_code)


class UserAdministratorKelolaUserEditUserMahasiswaView(UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def update(self, request, username):
        try:
            jenis_praktikum_id = int(request.data.get("jenis_praktikum_id"))
            periode_id = int(request.data.get("periode_id"))
            new_username = request.data.get("username")
            new_full_name = request.data.get("full_name")
            new_npm = request.data.get("npm")
            email = request.data.get("email")
            username_supervisor_lembaga = request.data.get("username_supervisor_lembaga")
            username_supervisor_sekolah = request.data.get("username_supervisor_sekolah")
            if (jenis_praktikum_id > 0 and periode_id > 0):
                Administrator.objects.get(user=request.user)
                user_mahasiswa = User.objects.get(username=username)
                mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa)
                mahasiswa_praktikum_active = MahasiswaPraktikum.objects.get(mahasiswa=mahasiswa, status=True)

                periode_new = Periode.objects.get(pk=periode_id)
                if (username_supervisor_lembaga != ''):
                    user_supervisor_lembaga_new = User.objects.get(username=username_supervisor_lembaga)
                    supervisor_lembaga_new = SupervisorLembaga.objects.get(user=user_supervisor_lembaga_new)
                else:
                    supervisor_lembaga_new = None

                if (username_supervisor_sekolah != ''):
                    user_supervisor_sekolah_new = User.objects.get(username=username_supervisor_sekolah)
                    supervisor_sekolah_new = SupervisorSekolah.objects.get(user=user_supervisor_sekolah_new)
                else:
                    supervisor_sekolah_new = None

                praktikum_new = Praktikum.objects.get(pk=jenis_praktikum_id)
                mahasiswa_praktikum_selected = MahasiswaPraktikum.objects.get(mahasiswa=mahasiswa, list_praktikum=praktikum_new)

                mahasiswa_praktikum_active.status = False
                mahasiswa_praktikum_active.save()

                mahasiswa_praktikum_selected.status = True
                mahasiswa_praktikum_selected.save()

                user_mahasiswa.username = new_username
                user_mahasiswa.email = email
                user_mahasiswa.full_name = new_full_name
                user_mahasiswa.save()

                mahasiswa.periode = periode_new
                mahasiswa.npm = new_npm
                mahasiswa.supervisor_lembaga = supervisor_lembaga_new
                mahasiswa.supervisor_sekolah = supervisor_sekolah_new
                mahasiswa.save()

                status_code = status.HTTP_200_OK
                response = {
                    response_field[0]: 'True',
                    response_field[1]: status_code,
                    response_field[2]: 'Data mahasiswa updated successfully',
                }
            else:
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                response = {
                    response_field[0]: 'False',
                    response_field[1]: status_code,
                    response_field[2]: 'Please enter a valid data input for id',
                }
        except ValueError:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Please enter a valid data input for id (int)',
            }
        except TypeError:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Please enter a valid field name for input',
            }
        except IntegrityError:
            status_code = status.HTTP_409_CONFLICT
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Duplication data for username or email',
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_administrator
            }
        except SupervisorSekolah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_supervisor_sekolah
            }
        except SupervisorLembaga.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_supervisor_lembaga
            }
        except Mahasiswa.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_mahasiswa
            }
        except MahasiswaPraktikum.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Can not find any data of kelola mahasiswa praktikum for mahasiswa'
            }
        except Praktikum.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Can not find any data of praktikum'
            }
        return Response(response, status=status_code)


class UserAdministratorGetAllUserMahasiswaView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            profile = Administrator.objects.get(user=request.user)
            mahasiswa = Mahasiswa.objects.all()
            mahasiswa_serializer = MahasiswaSerializer(mahasiswa, context={'request': request},
                                            many=True)

            user_serializer = AdministratorSerializer(profile, context={'request': request})

            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'List all supervisor sekolah fetch successfully',
                'data': mahasiswa_serializer.data,
                'user': user_serializer.data

            }

        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_administrator
            }

        return Response(response, status=status_code)


class UserAdministratorKelolaUserDetailUserSupervisorSekolahView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, username):
        try:
            profile = Administrator.objects.get(user=request.user)
            user_supervisor_sekolah = User.objects.get(username=username)
            supervisor_sekolah = SupervisorSekolah.objects.get(user=user_supervisor_sekolah)

            supervisor_sekolah_serializer = SupervisorSekolahListMahasiswaSerializer(supervisor_sekolah, context={'request': request})
            user_serializer = AdministratorSerializer(profile, context={'request': request})
            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Detail kelola supervisor sekolah fetch successfully',
                'data': supervisor_sekolah_serializer.data,
                'user': user_serializer.data
            }
        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_administrator
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        except SupervisorSekolah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_supervisor_sekolah
            }
        return Response(response, status=status_code)


class UserAdministratorKelolaUserEditUserSupervisorSekolahView(UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def update(self, request, username):
        try:
            new_username = request.data.get("username")
            new_full_name = request.data.get("full_name")
            email = request.data.get("email")
            role = request.data.get("role")
            Administrator.objects.get(user=request.user)
            user_supervisor_sekolah = User.objects.get(username=username)
            supervisor_sekolah = SupervisorSekolah.objects.get(user=user_supervisor_sekolah)

            user_supervisor_sekolah.username = new_username
            user_supervisor_sekolah.full_name = new_full_name
            user_supervisor_sekolah.email = email
            user_supervisor_sekolah.save()

            if role == Role.KKL.value:
                user_supervisor_sekolah.save()
                KoordinatorKuliah.objects.create(
                    user=user_supervisor_sekolah,
                    nip=supervisor_sekolah.nip
                )
                mahasiswa_bimbingan = Mahasiswa.objects.filter(supervisor_sekolah=supervisor_sekolah)
                mahasiswa_bimbingan.update(supervisor_sekolah=None)
                supervisor_sekolah.delete()
                status_code = status.HTTP_200_OK
                response = {
                    response_field[0]: 'True',
                    response_field[1]: status_code,
                    response_field[2]: 'Data supervisor sekolah updated successfully',
                }
            elif role == Role.SSK.value:
                status_code = status.HTTP_200_OK
                response = {
                    response_field[0]: 'True',
                    response_field[1]: status_code,
                    response_field[2]: 'Data supervisor sekolah updated successfully',
                }
            elif role == Role.ADM.value:
                user_supervisor_sekolah.save()
                Administrator.objects.create(
                    user=user_supervisor_sekolah,
                    nip=user_supervisor_sekolah.nip
                )
                mahasiswa_bimbingan = Mahasiswa.objects.filter(supervisor_sekolah=supervisor_sekolah)
                mahasiswa_bimbingan.update(supervisor_sekolah=None)
                supervisor_sekolah.delete()
                status_code = status.HTTP_200_OK
                response = {
                    response_field[0]: 'True',
                    response_field[1]: status_code,
                    response_field[2]: 'Data supervisor sekolah updated successfully',
                }
            else:
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                response = {
                    response_field[0]: 'False',
                    response_field[1]: status_code,
                    response_field[2]: 'Please enter a valid data input for role',
                }

        except TypeError:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Please enter a valid field name for input',
            }
        except IntegrityError:
            status_code = status.HTTP_409_CONFLICT
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Duplication data for username or email',
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_administrator
            }
        except SupervisorSekolah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_supervisor_sekolah
            }
        return Response(response, status=status_code)


class UserAdministratorGetAllUserSupervisorSekolahView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            profile = Administrator.objects.get(user=request.user)
            supervisor_sekolahs = SupervisorSekolah.objects.all()
            supervisor_sekolah_serializer = SupervisorSekolahSerializer(supervisor_sekolahs, context={'request': request},
                                            many=True)

            user_serializer = AdministratorSerializer(profile, context={'request': request})

            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'List all supervisor sekolah fetch successfully',
                'data': supervisor_sekolah_serializer.data,
                'user': user_serializer.data

            }

        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_administrator
            }

        return Response(response, status=status_code)


class UserAdministratorKelolaUserDetailUserSupervisorLembagaView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, username):
        try:
            profile = Administrator.objects.get(user=request.user)
            user_supervisor_lembaga = User.objects.get(username=username)
            supervisor_lembaga = SupervisorLembaga.objects.get(user=user_supervisor_lembaga)

            supervisor_lembaga_serializer = SupervisorLembagaListMahasiswaSerializer(supervisor_lembaga, context={'request': request})
            user_serializer = AdministratorSerializer(profile, context={'request': request})
            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Detail kelola supervisor lembaga fetch successfully',
                'data': supervisor_lembaga_serializer.data,
                'user': user_serializer.data
            }
        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_administrator
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        except SupervisorLembaga.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_supervisor_lembaga
            }
        return Response(response, status=status_code)


class UserAdministratorKelolaUserEditUserSupervisorLembagaView(UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def update(self, request, username):
        try:
            lembaga_id = int(request.data.get("lembaga_id"))
            username_baru = request.data.get("username")
            full_name_baru = request.data.get("full_name")
            jabatan = request.data.get("jabatan")
            email = request.data.get("email")
            is_active = request.data.get("is_active")

            if lembaga_id > 0:
                Administrator.objects.get(user=request.user)
                user_supervisor_lembaga = User.objects.get(username=username)
                supervisor_lembaga = SupervisorLembaga.objects.get(user=user_supervisor_lembaga)

                lembaga_new = Lembaga.objects.get(pk=lembaga_id)

                user_supervisor_lembaga.username = username_baru
                user_supervisor_lembaga.full_name = full_name_baru
                user_supervisor_lembaga.email = email
                user_supervisor_lembaga.is_active = is_active
                user_supervisor_lembaga.save()

                supervisor_lembaga.lembaga = lembaga_new
                supervisor_lembaga.jabatan = jabatan
                supervisor_lembaga.save()

                status_code = status.HTTP_200_OK
                response = {
                    response_field[0]: 'True',
                    response_field[1]: status_code,
                    response_field[2]: 'Data supervisor lembaga updated successfully',
                }
            else:
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                response = {
                    response_field[0]: 'False',
                    response_field[1]: status_code,
                    response_field[2]: 'Please enter a valid data input for id',
                }

        except ValueError:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Please enter a valid data input for id (int)',
            }
        except TypeError:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Please enter a valid field name for input',
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        except SupervisorLembaga.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_supervisor_lembaga
            }
        except Lembaga.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: "Lembaga id is not found"
            }
        except IntegrityError:
            status_code = status.HTTP_409_CONFLICT
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: "Duplicate value of username/email"
            }
        return Response(response, status=status_code)


class UserAdministratorKelolaUserDetailUserKoordinatorKuliahView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, username):
        try:
            profile = Administrator.objects.get(user=request.user)
            user_koordinator_kuliah = User.objects.get(username=username)
            koordinator_kuliah = KoordinatorKuliah.objects.get(user=user_koordinator_kuliah)

            koordinator_kuliah_serializer = KoordinatorKuliahListMahasiswaSerializer(koordinator_kuliah, context={'request': request})
            user_serializer = AdministratorSerializer(profile, context={'request': request})
            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Detail kelola koordinator kuliah fetch successfully',
                'data': koordinator_kuliah_serializer.data,
                'user': user_serializer.data
            }
        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_administrator
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        except KoordinatorKuliah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_koordinator_kuliah
            }
        return Response(response, status=status_code)


class UserAdministratorKelolaUserEditUserKoordinatorKuliahView(UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def update(self, request, username):
        try:
            new_username = request.data.get("username")
            new_full_name = request.data.get("full_name")
            email = request.data.get("email")
            role = request.data.get("role")
            Administrator.objects.get(user=request.user)
            user_koordinator_kuliah = User.objects.get(username=username)
            koordinator_kuliah = KoordinatorKuliah.objects.get(user=user_koordinator_kuliah)

            user_koordinator_kuliah.username = new_username
            user_koordinator_kuliah.full_name = new_full_name
            user_koordinator_kuliah.email = email
            user_koordinator_kuliah.save()

            if role == Role.SSK.value:
                user_koordinator_kuliah.save()
                SupervisorSekolah.objects.create(
                    user=user_koordinator_kuliah,
                    nip=koordinator_kuliah.nip
                )
                koordinator_kuliah.delete()
                status_code = status.HTTP_200_OK
                response = {
                    response_field[0]: 'True',
                    response_field[1]: status_code,
                    response_field[2]: 'Data koordinator kuliah updated successfully',
                }
            elif role == Role.KKL.value:
                status_code = status.HTTP_200_OK
                response = {
                    response_field[0]: 'True',
                    response_field[1]: status_code,
                    response_field[2]: 'Data koordinator kuliah updated successfully',
                }
            elif role == Role.ADM.value:
                user_koordinator_kuliah.save()
                Administrator.objects.create(
                    user=user_koordinator_kuliah,
                    nip=koordinator_kuliah.nip
                )
                koordinator_kuliah.delete()
                status_code = status.HTTP_200_OK
                response = {
                    response_field[0]: 'True',
                    response_field[1]: status_code,
                    response_field[2]: 'Data koordinator kuliah updated successfully',
                }
            else:
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                response = {
                    response_field[0]: 'False',
                    response_field[1]: status_code,
                    response_field[2]: 'Please enter a valid data input for role',
                }

        except TypeError:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Please enter a valid field name for input',
            }
        except IntegrityError:
            status_code = status.HTTP_409_CONFLICT
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Duplication data for username or email',
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_administrator
            }
        except KoordinatorKuliah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_koordinator_kuliah
            }
        return Response(response, status=status_code)


class UserAdministratorKelolaUserDetailUserAdministratorView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, username):
        try:
            profile = Administrator.objects.get(user=request.user)
            user_administrator = User.objects.get(username=username)
            administrator = Administrator.objects.get(user=user_administrator)

            administrator_serializer = AdministratorSerializer(administrator, context={'request': request})
            user_serializer = AdministratorSerializer(profile, context={'request': request})
            status_code = status.HTTP_200_OK
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Detail kelola administrator fetch successfully',
                'data': administrator_serializer.data,
                'user': user_serializer.data
            }
        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_administrator
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        return Response(response, status=status_code)


class UserAdministratorKelolaUserEditUserAdministratorView(UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def update(self, request, username):
        try:
            new_username = request.data.get("username")
            new_full_name = request.data.get("full_name")
            email = request.data.get("email")
            role = request.data.get("role")
            Administrator.objects.get(user=request.user)
            user_administrator = User.objects.get(username=username)
            administrator = Administrator.objects.get(user=user_administrator)

            user_administrator.username = new_username
            user_administrator.full_name = new_full_name
            user_administrator.email = email
            user_administrator.save()

            if role == Role.SSK.value:
                user_administrator.save()
                SupervisorSekolah.objects.create(
                    user=user_administrator,
                    nip=administrator.nip
                )
                administrator.delete()
                status_code = status.HTTP_200_OK
                response = {
                    response_field[0]: 'True',
                    response_field[1]: status_code,
                    response_field[2]: 'Data administrator updated successfully',
                }
            elif role == Role.ADM.value:
                status_code = status.HTTP_200_OK
                response = {
                    response_field[0]: 'True',
                    response_field[1]: status_code,
                    response_field[2]: 'Data administrator updated successfully',
                }
            elif role == Role.KKL.value:
                user_administrator.save()
                KoordinatorKuliah.objects.create(
                    user=user_administrator,
                    nip=administrator.nip
                )
                administrator.delete()
                status_code = status.HTTP_200_OK
                response = {
                    response_field[0]: 'True',
                    response_field[1]: status_code,
                    response_field[2]: 'Data administrator updated successfully',
                }
            else:
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                response = {
                    response_field[0]: 'False',
                    response_field[1]: status_code,
                    response_field[2]: 'Please enter a valid data input for role',
                }

        except TypeError:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Please enter a valid field name for input',
            }
        except IntegrityError:
            status_code = status.HTTP_409_CONFLICT
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Duplication data for username or email',
            }
        except User.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_user
            }
        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_administrator
            }
        return Response(response, status=status_code)


# Temporary for sprint review lol
class MahasiswaPraktikumView(viewsets.ModelViewSet):
    """
    Provides a get method handler.
    """
    permission_classes = (AllowAny, )
    queryset = MahasiswaPraktikum.objects.all()
    serializer_class = MahasiswaDetailPraktikumSerializerTemp


class LaporanAkhirDBView(views.APIView):
    """
    Provides a get method handler.
    """
    permission_classes = (AllowAny, )

    def get(self, request):
        final_queryset = []
        mahasiswa = Mahasiswa.objects.all()
        for mhs in mahasiswa:
            laporan_akhir = LaporanAkhirPraktikum.objects.filter(mahasiswa=mhs)
            data = {}
            data['mahasiswa'] = MahasiswaSerializer(mhs).data
            data['laporan_akhir'] = []
            for lprn in laporan_akhir:
                data['laporan_akhir'].append(LaporanAkhirPraktikumSerializer_v2(lprn).data)
            final_queryset.append(data)
        return Response(final_queryset)


class LaporanAkhirPraktikumView(viewsets.ModelViewSet):
    """
    Provides a get method handler.
    """
    permission_classes = (AllowAny, )
    serializer_class = LaporanAkhirPraktikumSerializer
    queryset = LaporanAkhirPraktikum.objects.all()

    def create(self, request):
        npm = request.data['npm_mahasiswa']
        praktikum_ke = request.data['jenis_praktikum']
        data = request.data['file']
        lembaga_id = request.data['lembaga_id']
        frmt, filestr = data.split(';base64,')
        ext = frmt.split('/')[-1]

        obj, created = LaporanAkhirPraktikum.objects.update_or_create(
            nama_laporan=request.data['nama_laporan'],
            waktu_deadline=datetime.now(),
            mahasiswa=Mahasiswa.objects.get(npm=npm),
            jenis_praktikum=Praktikum.objects.get(jenis_praktikum=praktikum_ke),
            periode_praktikum=request.data['periode_praktikum'],
            lembaga=Lembaga.objects.get(id=lembaga_id),
            laporan_akhir=ContentFile(base64.b64decode(filestr), name=npm + '.' + ext),
            umpan_balik='default',
            status_publikasi=True
        )
        return HttpResponse('OK')

    def update(self, request, pk):
        npm = request.data['npm_mahasiswa']
        praktikum_ke = request.data['jenis_praktikum']
        data = request.data['file']
        lembaga_id = request.data['lembaga_id']
        frmt, filestr = data.split(';base64,')
        ext = frmt.split('/')[-1]

        LaporanAkhirPraktikum.objects.filter(pk=pk).update(
            nama_laporan=request.data['nama_laporan'],
            waktu_deadline=datetime.now(),
            mahasiswa=Mahasiswa.objects.get(npm=npm),
            jenis_praktikum=Praktikum.objects.get(jenis_praktikum=praktikum_ke),
            periode_praktikum=request.data['periode_praktikum'],
            lembaga=Lembaga.objects.get(id=lembaga_id),
            umpan_balik='default'
        )

        lprn = LaporanAkhirPraktikum.objects.get(pk=pk)
        lprn.laporan_akhir = ContentFile(base64.b64decode(filestr), name=npm + '.' + ext)
        lprn.save()
        return HttpResponse('OK')


class MahasiswaView(viewsets.ModelViewSet):
    """
    API For Mahasiswa List,
    Sorted in Alphabetical Order

    Usage:


    npm (Optional) = Mahasiswa's NPM
    """

    # Authentication Setting
    permission_classes = (AllowAny, )

    # Initialize Serializer for Mahasiswa
    serializer_class = MahasiswaWithJenisPraktikumSerializer

    # Retrieve objects from models in alphabetical order (default)
    queryset = Mahasiswa.objects.order_by('user__username')

    # The method below handles data retrieval
    # when filter parameter is applied
    def get_queryset(self, *args, **kwargs):
        result = dict()
        try:
            """
            Optionally restricts the returned Mahasiswas
            by filtering against a `npm` query parameter in the URL.
            """

            # Retrieve objects from models in alphabetical order
            queryset = Mahasiswa.objects.order_by('user__username')

            # Parameter to retrieve data by filter (npm)
            parameter = self.request.GET.get('npm')

            # Check if it uses parameter to filter data
            if (parameter):
                queryset = queryset.filter(npm=parameter)

            # Return JSON Response
            return queryset

        # HANDLE EXCEPTION when there is Unicode Error
        except UnicodeError:
            # Build JSON Response
            result['status'] = "500"
            result['message'] = "Unable to handle Unicode Input."
            return result

        # HANDLE EXCEPTION when NameError (undefined variables, undefined data, etc) occured
        except NameError:
            # Build JSON Response
            result['status'] = "500"
            result['message'] = "Undefined data occured, please check the given parameters, etc."
            return result

        # HANDLE EXCEPTION when no data is found
        except Mahasiswa.DoesNotExist:
            # Build JSON Response
            result['status'] = "404"
            result['message'] = "Mahasiswa not found based on the given filter!"
            return result


class InputDataMahasiswaExcelView(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    excel_columns = [
        'No',
        'Nama Awal',
        'Nama Akhir',
        'Username SSO',
        'Email UI',
        'NPM',
        'Jenis Praktikum',
        'Username Supervisor Sekolah',
        'Username Supervisor Lembaga',
        'Lembaga',
        'Periode'
    ]
    number_of_laporan = 14
    template_laporan_name = "Laporan Minggu "
    template_laporan_akhir_name = "Laporan Akhir"
    template_laporan_borang_name = "Borang Penilaian Praktikum"

    def post(self, request):
        try:
            Administrator.objects.get(user=request.user)
            excel_file = request.data['file']
            if (str(excel_file).split('.')[-1] == 'xls'):
                data = xls_get(excel_file, column_limit=len(self.excel_columns))

                is_saved_file_name = (Config.objects.filter(key="file_name_sheet_mahasiswa").count() != 0)
                if is_saved_file_name:
                    file_name = Config.objects.get(key="file_name_sheet_mahasiswa")
                    file_name.value = str(excel_file)
                    file_name.save()
                else:
                    Config.objects.create(
                        key="file_name_sheet_mahasiswa",
                        value=str(excel_file)
                    )

                is_saved_file_date = (Config.objects.filter(key="file_date_sheet_mahasiswa").count() != 0)
                if is_saved_file_date:
                    file_date = Config.objects.get(key="file_date_sheet_mahasiswa")
                    file_date.value = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
                    file_date.save()
                else:
                    Config.objects.create(
                        key="file_date_sheet_mahasiswa",
                        value=datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
                    )

            elif (str(excel_file).split('.')[-1] == 'xlsx'):
                data = xlsx_get(excel_file, column_limit=len(self.excel_columns))

                is_saved_file_name = (Config.objects.filter(key="file_name_sheet_mahasiswa").count() != 0)
                if is_saved_file_name:
                    file_name = Config.objects.get(key="file_name_sheet_mahasiswa")
                    file_name.value = str(excel_file)
                    file_name.save()
                else:
                    Config.objects.create(
                        key="file_name_sheet_mahasiswa",
                        value=str(excel_file)
                    )

                is_saved_file_date = (Config.objects.filter(key="file_date_sheet_mahasiswa").count() != 0)
                if is_saved_file_date:
                    file_date = Config.objects.get(key="file_date_sheet_mahasiswa")
                    file_date.value = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
                    file_date.save()
                else:
                    Config.objects.create(
                        key="file_date_sheet_mahasiswa",
                        value=datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
                    )

            else:
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                response = {
                    response_field[0]: 'False',
                    response_field[1]: status_code,
                    response_field[2]: 'Please enter a valid format xls or xlsx file',
                }

            file_name, mahasiswa_list = list(data.items())[0]
            mahasiswa_list = mahasiswa_list[1:]
            if (len(mahasiswa_list) >= 1):

                for mahasiswa in mahasiswa_list:

                    try:
                        if mahasiswa == []:
                            break
                        if len(mahasiswa) < 11:
                            break
                    except IndexError:
                        break

                    if (len(mahasiswa) == len(self.excel_columns)) and (mahasiswa[0] != self.excel_columns[0]):
                        username_count = User.objects.filter(username=mahasiswa[self.excel_columns.index('Username SSO')]).count()
                        email_count = User.objects.filter(email=mahasiswa[self.excel_columns.index('Email UI')]).count()
                        try:
                            user_supervisor_sekolah = User.objects.get(username=mahasiswa[self.excel_columns.index('Username Supervisor Sekolah')])
                            supervisor_sekolah = SupervisorSekolah.objects.get(user=user_supervisor_sekolah)
                        except User.DoesNotExist:
                            supervisor_sekolah = None
                        except SupervisorSekolah.DoesNotExist:
                            supervisor_sekolah = None

                        try:
                            user_supervisor_lembaga = User.objects.get(username=mahasiswa[self.excel_columns.index('Username Supervisor Lembaga')])
                            supervisor_lembaga = SupervisorLembaga.objects.get(user=user_supervisor_lembaga)
                        except User.DoesNotExist:
                            supervisor_lembaga = None
                        except SupervisorLembaga.DoesNotExist:
                            supervisor_lembaga = None
                        try:
                            periode = Periode.objects.get(nama=mahasiswa[self.excel_columns.index('Periode')])
                        except Periode.DoesNotExist:
                            periode = Periode.objects.create(nama=mahasiswa[self.excel_columns.index('Periode')])

                        if (username_count == 0) and (email_count == 0):
                            user = User.objects.create_user(
                                first_name=mahasiswa[self.excel_columns.index('Nama Awal')],
                                last_name=mahasiswa[self.excel_columns.index('Nama Akhir')],
                                username=mahasiswa[self.excel_columns.index('Username SSO')],
                                email=mahasiswa[self.excel_columns.index('Email UI')],
                            )

                            mahasiswa_object = Mahasiswa.objects.create(
                                user=user,
                                npm=mahasiswa[self.excel_columns.index('NPM')],
                                supervisor_sekolah=supervisor_sekolah,
                                supervisor_lembaga=supervisor_lembaga,
                                periode=periode
                            )
                        else:
                            user = User.objects.get(username=mahasiswa[self.excel_columns.index('Username SSO')])
                            user.email = mahasiswa[self.excel_columns.index('Email UI')]
                            user.is_active = True
                            user.save()

                            mahasiswa_object = Mahasiswa.objects.get(user=user)
                            mahasiswa_object.npm = mahasiswa[self.excel_columns.index('NPM')]
                            mahasiswa_object.supervisor_sekolah = supervisor_sekolah
                            mahasiswa_object.supervisor_lembaga = supervisor_lembaga
                            mahasiswa_object.periode = periode
                            mahasiswa_object.save()

                        praktikum_list = Praktikum.objects.all()
                        mahasiswa_praktikum = MahasiswaPraktikum.objects.filter(mahasiswa=mahasiswa_object).count()
                        for praktikum in praktikum_list:
                            if praktikum.jenis_praktikum == mahasiswa[self.excel_columns.index('Jenis Praktikum')]:
                                is_active = True
                            else:
                                is_active = False

                            if mahasiswa_praktikum == 0:
                                MahasiswaPraktikum.objects.create(
                                    mahasiswa=mahasiswa_object,
                                    list_praktikum=praktikum,
                                    status=is_active
                                )
                            else:
                                MahasiswaPraktikum.objects.filter(mahasiswa=mahasiswa_object, list_praktikum=praktikum).update(status=is_active)

                            laporan_count = KelolaLaporanPraktikum.objects.filter(mahasiswa=mahasiswa_object, jenis_praktikum=praktikum).count()
                            if is_active and laporan_count == 0:
                                for i in range(1, self.number_of_laporan + 1):
                                    KelolaLaporanPraktikum.objects.create(
                                        mahasiswa=mahasiswa_object,
                                        jenis_praktikum=praktikum,
                                        nama_laporan=self.template_laporan_name + str(i)
                                    )

                            laporan_akhir_count = LaporanAkhirPraktikum.objects.filter(mahasiswa=mahasiswa_object, jenis_praktikum=praktikum).count()
                            if is_active and laporan_akhir_count == 0:
                                LaporanAkhirPraktikum.objects.create(
                                    mahasiswa=mahasiswa_object,
                                    jenis_praktikum=praktikum,
                                    nama_laporan=self.template_laporan_akhir_name
                                )

                            laporan_borang_count = LaporanBorangPraktikum.objects.filter(mahasiswa=mahasiswa_object, jenis_praktikum=praktikum).count()
                            if is_active and laporan_borang_count == 0:
                                LaporanBorangPraktikum.objects.create(
                                    mahasiswa=mahasiswa_object,
                                    jenis_praktikum=praktikum,
                                    nama_laporan=self.template_laporan_borang_name
                                )

            status_code = status.HTTP_201_CREATED
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Successfuly added to database',
            }
        except MultiValueDictKeyError:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Please enter a valid format row-column excel file',
            }
        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_administrator
            }
        return Response(response, status=status_code)


class InputDataDosenExcelView(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    excel_columns = [
        'No',
        'Nama Awal',
        'Nama Akhir',
        'Username SSO',
        'Email UI',
        'Role',
        'NIP'
    ]

    def post(self, request):
        try:
            Administrator.objects.get(user=request.user)
            excel_file = request.data['file']
            if (str(excel_file).split('.')[-1] == 'xls'):
                data = xls_get(excel_file, column_limit=len(self.excel_columns))

                is_saved_file_name = (Config.objects.filter(key="file_name_sheet_dosen").count() != 0)
                if is_saved_file_name:
                    file_name = Config.objects.get(key="file_name_sheet_dosen")
                    file_name.value = str(excel_file)
                    file_name.save()
                else:
                    Config.objects.create(
                        key="file_name_sheet_dosen",
                        value=str(excel_file)
                    )

                is_saved_file_date = (Config.objects.filter(key="file_date_sheet_dosen").count() != 0)
                if is_saved_file_date:
                    file_date = Config.objects.get(key="file_date_sheet_dosen")
                    file_date.value = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
                    file_date.save()
                else:
                    Config.objects.create(
                        key="file_date_sheet_dosen",
                        value=datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
                    )

            elif (str(excel_file).split('.')[-1] == 'xlsx'):
                data = xlsx_get(excel_file, column_limit=len(self.excel_columns))

                is_saved_file_name = (Config.objects.filter(key="file_name_sheet_dosen").count() != 0)
                if is_saved_file_name:
                    file_name = Config.objects.get(key="file_name_sheet_dosen")
                    file_name.value = str(excel_file)
                    file_name.save()
                else:
                    Config.objects.create(
                        key="file_name_sheet_dosen",
                        value=str(excel_file)
                    )

                is_saved_file_date = (Config.objects.filter(key="file_date_sheet_dosen").count() != 0)
                if is_saved_file_date:
                    file_date = Config.objects.get(key="file_date_sheet_dosen")
                    file_date.value = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
                    file_date.save()
                else:
                    Config.objects.create(
                        key="file_date_sheet_dosen",
                        value=datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
                    )

            else:
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                response = {
                    response_field[0]: 'False',
                    response_field[1]: status_code,
                    response_field[2]: 'Please enter a valid format xls or xlsx file',
                }

            file_name, dosen_list = list(data.items())[0]
            dosen_list = dosen_list[1:]
            if (len(dosen_list) >= 1):

                for dosen in dosen_list:

                    try:
                        if dosen == []:
                            break
                        if len(dosen) < 7:
                            break
                    except IndexError:
                        break

                    role = dosen[self.excel_columns.index('Role')]

                    if (len(dosen) == len(self.excel_columns)) and (dosen[0] != self.excel_columns[0]) and \
                            ((role == Role.SSK.value) or (role == Role.KKL.value) or (role == Role.ADM.value)):

                        username_count = User.objects.filter(username=dosen[self.excel_columns.index('Username SSO')]).count()
                        email_count = User.objects.filter(email=dosen[self.excel_columns.index('Email UI')]).count()

                        if (username_count == 0) and (email_count == 0):
                            user = User.objects.create_user(
                                first_name=dosen[self.excel_columns.index('Nama Awal')],
                                last_name=dosen[self.excel_columns.index('Nama Akhir')],
                                username=dosen[self.excel_columns.index('Username SSO')],
                                email=dosen[self.excel_columns.index('Email UI')],
                            )
                            if role == Role.SSK.value:
                                dosen_object = SupervisorSekolah.objects.create(
                                    user=user,
                                    nip=dosen[self.excel_columns.index('NIP')]
                                )
                            if role == Role.KKL.value:
                                dosen_object = KoordinatorKuliah.objects.create(
                                    user=user,
                                    nip=dosen[self.excel_columns.index('NIP')]
                                )
                            if role == Role.KKL.value:
                                dosen_object = Administrator.objects.create(
                                    user=user,
                                    nip=dosen[self.excel_columns.index('NIP')]
                                )
                        else:
                            user = User.objects.get(username=dosen[self.excel_columns.index('Username SSO')])
                            if Administrator.objects.filter(user=user).count() != 0:
                                old_role = "Administrator"
                            elif SupervisorSekolah.objects.filter(user=user).count() != 0:
                                old_role = "Supervisor Sekolah"
                            elif KoordinatorKuliah.objects.filter(user=user).count() != 0:
                                old_role = "Koordinator Praktikum"
                            user.email = dosen[self.excel_columns.index('Email UI')]
                            user.role = role
                            user.is_active = True
                            user.save()

                            if old_role == Role.SSK.value:
                                dosen_object = SupervisorSekolah.objects.get(user=user)
                            elif old_role == Role.KKL.value:
                                dosen_object = KoordinatorKuliah.objects.get(user=user)
                            elif old_role == Role.ADM.value:
                                dosen_object = Administrator.objects.get(user=user)

                            dosen_object.nip = dosen[self.excel_columns.index('NIP')]
                            dosen_object.save()

                            if old_role != role:
                                if role == Role.SSK.value:
                                    SupervisorSekolah.objects.create(
                                        user=user,
                                        nip=dosen_object.nip
                                    )
                                elif role == Role.KKL.value:
                                    KoordinatorKuliah.objects.create(
                                        user=user,
                                        nip=dosen_object.nip
                                    )
                                elif role == Role.ADM.value:
                                    Administrator.objects.create(
                                        user=user,
                                        nip=dosen_object.nip
                                    )
                                dosen_object.delete()

            status_code = status.HTTP_201_CREATED
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: 'Successfuly added to database',
            }
        except MultiValueDictKeyError:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Please enter a valid format row-column excel file',
            }
        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: error_message_404_administrator
            }
        return Response(response, status=status_code)


class UserAdministratorFileUploadInfo(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        sheet_name_dosen_exist = (Config.objects.filter(key="file_name_sheet_dosen").count() != 0)
        sheet_date_dosen_exist = (Config.objects.filter(key="file_date_sheet_dosen").count() != 0)
        sheet_name_mahasiswa_exist = (Config.objects.filter(key="file_name_sheet_mahasiswa").count() != 0)
        sheet_date_mahasiswa_exist = (Config.objects.filter(key="file_date_sheet_mahasiswa").count() != 0)

        sheet_name_dosen = ""
        sheet_date_dosen = ""
        sheet_name_mahasiswa = ""
        sheet_date_mahasiswa = ""

        if sheet_name_dosen_exist:
            sheet_name_dosen = Config.objects.get(key="file_name_sheet_dosen").value
        if sheet_date_dosen_exist:
            sheet_date_dosen = Config.objects.get(key="file_date_sheet_dosen").value
        if sheet_name_mahasiswa_exist:
            sheet_name_mahasiswa = Config.objects.get(key="file_name_sheet_mahasiswa").value
        if sheet_date_mahasiswa_exist:
            sheet_date_mahasiswa = Config.objects.get(key="file_date_sheet_mahasiswa").value

        status_code = status.HTTP_200_OK
        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            'file_name_dosen': sheet_name_dosen,
            'file_date_dosen': sheet_date_dosen,
            'file_name_mahasiswa': sheet_name_mahasiswa,
            'file_date_mahasiswa': sheet_date_mahasiswa
        }
        return Response(response, status=status_code)
