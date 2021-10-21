from authentication.models import (
    User,
    Mahasiswa,
    SupervisorLembaga,
    SupervisorSekolah,
    Periode
)
from authentication.serializers import (
    MahasiswaSerializer,
    SupervisorLembagaSerializer,
    SupervisorSekolahSerializer
)

from lembaga.models import (
    Lembaga,
    Institusi,
    Tema
)

from laporan_praktikum.models import (
    Praktikum,
    KelolaLaporanPraktikum,
    LaporanAkhirPraktikum,
    LaporanBorangPraktikum,
    MahasiswaPraktikum,
    Praktikum
)
from laporan_praktikum.serializers import (
    KelolaLaporanPraktikumSerializer,
    KelolaLaporanPraktikumDefaultSerializer,
    MahasiswaDetailPraktikumSerializer,
    PraktikumSerializer,

    RiwayatMahasiswaLaporanMingguanSerializer,
    RiwayatMahasiswaLaporanAkhirSerializer,
    RiwayatMahasiswaLaporanBorangSerializer,

    RiwayatSupervisiMahasiswaBySupervisorLembagaSerializer,
    RiwayatSupervisiLaporanAkhirMahasiswaBySupervisorLembagaSerializer,
    RiwayatSupervisiLaporanBorangMahasiswaBySupervisorLembagaSerializer,

    RiwayatSupervisiMahasiswaBySupervisorSekolahSerializer,
    RiwayatSupervisiLaporanAkhirMahasiswaBySupervisorSekolahSerializer,
    RiwayatSupervisiLaporanBorangMahasiswaBySupervisorSekolahSerializer,

    RiwayatSupervisiMahasiswaWithContextProfileSerializer,
    SupervisorSekolahListMahasiswaSerializer,
    SupervisorLembagaSpesificSerializer,
    RiwayatSupervisiMahasiswaLaporanAkhirWithContextProfileSerializer,
    RiwayatSupervisiMahasiswaLaporanBorangWithContextProfileSerializer

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

from django.core import serializers
from django.db import transaction, IntegrityError
from django.http import HttpResponse, JsonResponse

import json
import datetime
from dateutil.parser import parse

response_field = ['success', 'status_code', 'message']

# Messages
STR_SUCCESS_FETCH_LAPORAN_PRAKTIKUM = "Laporan Praktikum fetched successfully"


@api_view(["GET"])  # pragma: no cover
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_riwayat_laporan_by_mahasiswa(request):
    # Mahasiswa Riwayat Laporan Terunggah
    mahasiswa = Mahasiswa.objects.get(user=request.user)
    praktikum = MahasiswaPraktikum.objects.get(mahasiswa=mahasiswa, status=True)
    laporan_mingguan_mahasiswa = KelolaLaporanPraktikum.objects.filter(mahasiswa=mahasiswa,
                                jenis_praktikum=praktikum.list_praktikum)
    laporan_akhir_mahasiswa = LaporanAkhirPraktikum.objects.filter(mahasiswa=mahasiswa,
                                jenis_praktikum=praktikum.list_praktikum)
    laporan_borang_mahasiswa = LaporanBorangPraktikum.objects.filter(mahasiswa=mahasiswa,
                                jenis_praktikum=praktikum.list_praktikum)

    serializer_mahasiswa = MahasiswaSerializer(mahasiswa, context={'request': request})

    serializer_riwayat_laporan_mingguan = RiwayatMahasiswaLaporanMingguanSerializer(
        laporan_mingguan_mahasiswa.order_by('-waktu_submisi'),
        context={'request': request}, many=True)
    serializers_riwayat_laporan_akhir = RiwayatMahasiswaLaporanAkhirSerializer(
        laporan_akhir_mahasiswa.order_by('-waktu_submisi'),
        context={'request': request}, many=True)
    serializer_riwayat_laporan_borang = RiwayatMahasiswaLaporanBorangSerializer(
        laporan_borang_mahasiswa.order_by('-waktu_submisi'),
        context={'request': request}, many=True)

    serializer_riwayat_lap_mingguan_supv_lembaga = RiwayatSupervisiMahasiswaBySupervisorLembagaSerializer(
        laporan_mingguan_mahasiswa.order_by('-waktu_nilai_supv_lembaga'),
        context={'request': request}, many=True)
    serializer_riwayat_lap_akhir_supv_lembaga = RiwayatSupervisiLaporanAkhirMahasiswaBySupervisorLembagaSerializer(
        laporan_akhir_mahasiswa.order_by('-waktu_nilai_supv_lembaga'),
        context={'request': request}, many=True)
    serializer_riwayat_lap_borang_supv_lembaga = RiwayatSupervisiLaporanBorangMahasiswaBySupervisorLembagaSerializer(
        laporan_borang_mahasiswa.order_by('-waktu_nilai_supv_lembaga'),
        context={'request': request}, many=True)

    serializer_riwayat_lap_mingguan_supv_sekolah = RiwayatSupervisiMahasiswaBySupervisorSekolahSerializer(
        laporan_mingguan_mahasiswa.order_by('-waktu_nilai_supv_sekolah'),
        context={'request': request}, many=True)
    serializer_riwayat_lap_akhir_supv_sekolah = RiwayatSupervisiLaporanAkhirMahasiswaBySupervisorSekolahSerializer(
        laporan_akhir_mahasiswa.order_by('-waktu_nilai_supv_sekolah'),
        context={'request': request}, many=True)
    serializer_riwayat_lap_borang_supv_sekolah = RiwayatSupervisiLaporanBorangMahasiswaBySupervisorSekolahSerializer(
        laporan_borang_mahasiswa.order_by('-waktu_nilai_supv_sekolah'),
        context={'request': request}, many=True)

    status_code = status.HTTP_200_OK
    response = {
        response_field[0]: 'True',
        response_field[1]: status_code,
        response_field[2]: STR_SUCCESS_FETCH_LAPORAN_PRAKTIKUM,
        'profile': serializer_mahasiswa.data,
        'riwayat_laporan_siswa': {
            'laporan_mingguan': serializer_riwayat_laporan_mingguan.data,
            'laporan_akhir': serializers_riwayat_laporan_akhir.data,
            'laporan_borang': serializer_riwayat_laporan_borang.data
        },
        'riwayat_supv_sekolah': {
            'laporan_mingguan': serializer_riwayat_lap_mingguan_supv_sekolah.data,
            'laporan_akhir': serializer_riwayat_lap_akhir_supv_sekolah.data,
            'laporan_borang': serializer_riwayat_lap_borang_supv_sekolah.data
        },
        'riwayat_supv_lembaga': {
            'laporan_mingguan': serializer_riwayat_lap_mingguan_supv_lembaga.data,
            'laporan_akhir': serializer_riwayat_lap_akhir_supv_lembaga.data,
            'laporan_borang': serializer_riwayat_lap_borang_supv_lembaga.data
        }
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])  # pragma: no cover
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_riwayat_laporan_by_supervisor_sekolah(request):
    # Supervisor Sekolah Riwayat Laporan
    profile_supervisor_sekolah = SupervisorSekolah.objects.get(user=request.user)
    list_profile_mahasiswa = Mahasiswa.objects.filter(supervisor_sekolah=profile_supervisor_sekolah)

    data_laporan_mahasiswa = Mahasiswa.objects.none()
    data_laporan_akhir_mahasiswa = Mahasiswa.objects.none()
    data_laporan_borang_mahasiswa = Mahasiswa.objects.none()
    for profile_mahasiswa in list_profile_mahasiswa.iterator():

        praktikum = MahasiswaPraktikum.objects.get(mahasiswa=profile_mahasiswa, status=True)
        laporan_mahasiswa = KelolaLaporanPraktikum.objects.filter(mahasiswa=profile_mahasiswa, jenis_praktikum=praktikum.list_praktikum)
        laporan_akhir_mahasiswa = LaporanAkhirPraktikum.objects.filter(mahasiswa=profile_mahasiswa, jenis_praktikum=praktikum.list_praktikum)
        laporan_borang_mahasiswa = LaporanBorangPraktikum.objects.filter(mahasiswa=profile_mahasiswa, jenis_praktikum=praktikum.list_praktikum)

        # merge querysets
        data_laporan_mahasiswa = data_laporan_mahasiswa | laporan_mahasiswa
        data_laporan_akhir_mahasiswa = data_laporan_akhir_mahasiswa | laporan_akhir_mahasiswa
        data_laporan_borang_mahasiswa = data_laporan_borang_mahasiswa | laporan_borang_mahasiswa

    serializer_supervisor_sekolah = SupervisorSekolahSerializer(profile_supervisor_sekolah, context={'request': request})
    serializer_riwayat_mahasiswa = RiwayatSupervisiMahasiswaWithContextProfileSerializer(
        data_laporan_mahasiswa.order_by('skor_laporan_sekolah', '-waktu_submisi'),
        context={'request': request}, many=True)

    serializer_riwayat_lap_akhir = RiwayatSupervisiMahasiswaLaporanAkhirWithContextProfileSerializer(
        data_laporan_akhir_mahasiswa.order_by('skor_laporan_sekolah', '-waktu_submisi'),
        context={'request': request}, many=True)

    serializer_riwayat_lap_borang = RiwayatSupervisiMahasiswaLaporanAkhirWithContextProfileSerializer(
        data_laporan_borang_mahasiswa.order_by('skor_laporan_sekolah', '-waktu_submisi'),
        context={'request': request}, many=True)

    status_code = status.HTTP_200_OK
    response = {
        response_field[0]: 'True',
        response_field[1]: status_code,
        response_field[2]: STR_SUCCESS_FETCH_LAPORAN_PRAKTIKUM,
        'profile': serializer_supervisor_sekolah.data,
        'riwayat_laporan_siswa': serializer_riwayat_mahasiswa.data,
        'riwayat_laporan_akhir': serializer_riwayat_lap_akhir.data,
        'riwayat_laporan_borang': serializer_riwayat_lap_borang.data
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])  # pragma: no cover
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_riwayat_laporan_by_supervisor_lembaga(request):

    # Supervisor Lembaga Riwayat Laporan
    profile_supervisor_lembaga = SupervisorLembaga.objects.get(user=request.user)
    list_profile_mahasiswa = Mahasiswa.objects.filter(supervisor_lembaga=profile_supervisor_lembaga)

    data_laporan_mahasiswa = Mahasiswa.objects.none()
    for profile_mahasiswa in list_profile_mahasiswa.iterator():

        praktikum = MahasiswaPraktikum.objects.get(mahasiswa=profile_mahasiswa, status=True)
        laporan_mahasiswa = LaporanAkhirPraktikum.objects.filter(mahasiswa=profile_mahasiswa, jenis_praktikum=praktikum.list_praktikum)

        # merge querysets
        data_laporan_mahasiswa = data_laporan_mahasiswa | laporan_mahasiswa

    serializer_supervisor_lembaga = SupervisorLembagaSerializer(profile_supervisor_lembaga, context={'request': request})
    serializer_riwayat_mahasiswa = RiwayatSupervisiMahasiswaLaporanAkhirWithContextProfileSerializer(
        data_laporan_mahasiswa.order_by('skor_laporan_sekolah', '-waktu_submisi'),
        context={'request': request}, many=True)

    status_code = status.HTTP_200_OK
    response = {
        response_field[0]: 'True',
        response_field[1]: status_code,
        response_field[2]: STR_SUCCESS_FETCH_LAPORAN_PRAKTIKUM,
        'profile': serializer_supervisor_lembaga.data,
        'riwayat_laporan_siswa': serializer_riwayat_mahasiswa.data,
    }
    return Response(response, status=status.HTTP_200_OK)

# Django Views for Riwayat Praktikum by Lembaga


@api_view(["GET"])  # pragma: no cover
@authentication_classes([])
@permission_classes([])
def get_riwayat_laporan_by_lembaga(request):
    '''
    API Endpoint:
        http://localhost:8000/api/v1/lembaga/praktikum?lembaga=<string>

    Expected output:
        Lembaga and its riwayat laporan

    Output Format:
        success: boolean
        status_code: html status code
        data: JSON Data
    '''

    try:
        query_lembaga = request.GET.get('lembaga')
        lembaga_object = Lembaga.objects.get(pk=query_lembaga)

        # Periode
        if 'periode' in request.GET:
            periode = request.GET['periode']
        else:
            periode = "all"

        # Retrieve Laporan Akhir from Database
        laporan = LaporanAkhirPraktikum.objects.filter(lembaga=lembaga_object.id)

        # Convert laporan query to JSON
        laporan_list = []
        mahasiswas = set()
        for i in laporan:
            object_json = {}
            if i.periode_praktikum == periode or periode == "all":
                object_json['nama_laporan'] = i.nama_laporan
                object_json['jenis_praktikum'] = i.jenis_praktikum.jenis_praktikum
                object_json['mahasiswa'] = i.mahasiswa.user.username
                object_json['periode_praktikum'] = i.periode_praktikum
                laporan_list.append(object_json)
                mahasiswas.add(i.mahasiswa.user.username)

        status_code = status.HTTP_200_OK
        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: STR_SUCCESS_FETCH_LAPORAN_PRAKTIKUM,
            'data': laporan_list,
            'count': len(mahasiswas),
        }
    except Lembaga.DoesNotExist:
        # To indicate that Lembaga is not found and give clear info about the problem
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Lembaga cannot be found',
            'data': [],
            'count': 0,
        }
    except LaporanAkhirPraktikum.DoesNotExist:
        # To indicate that Riwayat Praktikum for this Lembaga is not found and give clear info about the problem
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Riwayat Praktikum for this Lembaga cannot be found',
            'data': [],
            'count': 0,
        }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])  # pragma: no cover
@authentication_classes([])
@permission_classes([])
def get_periode_list(request):
    '''
    API Endpoint:
        http://localhost:8000/api/v1/periode

    Expected output:
        List of all Periodes
    '''

    periode = [i.nama for i in Periode.objects.all()]

    status_code = status.HTTP_200_OK
    response = {
        response_field[0]: 'True',
        response_field[1]: status_code,
        response_field[2]: "Periodes has successfully been loaded",
        'data': periode,
        'count': len(periode),
    }
    return Response(response, status=status.HTTP_200_OK)


def get_ketepatan_pengumpulan_per_week():
    none_check = None

    # Retrieve Laporan from Database
    laporan = KelolaLaporanPraktikum.objects.filter(status_publikasi=True).order_by('waktu_deadline')
    # riwayat_ketepatan and total_pengumpulan are for output
    riwayat_ketepatan = dict()
    total_pengumpulan = dict()

    # First Week of the first submission
    one_laporan = laporan[0:1].get()
    first_week = datetime.date(one_laporan.waktu_deadline.year, one_laporan.waktu_deadline.month, one_laporan.waktu_deadline.day).isocalendar()[1]

    # First Year
    first_year = datetime.date(one_laporan.waktu_deadline.year, one_laporan.waktu_deadline.month, one_laporan.waktu_deadline.day).isocalendar()[0]

    # Iterate Through Laporan
    for one_laporan in laporan:
        # Check if Mahasiswa is active
        is_active = KelolaLaporanPraktikum.objects.filter(mahasiswa=one_laporan.mahasiswa, status_publikasi=True).count() > 0

        # Check if it has deadline and is active
        if (not is_active) and (not one_laporan.waktu_deadline):
            continue

        # Dictionary for counting this week's submission time
        this_weeks_laporan = {}
        this_weeks_laporan[True] = 0
        this_weeks_laporan[False] = 0

        # Get Week
        this_time = datetime.date(one_laporan.waktu_deadline.year, one_laporan.waktu_deadline.month, one_laporan.waktu_deadline.day).isocalendar()
        week = this_time[1]

        # Adjust week according to first week
        week = week - first_week + 1

        # Adjust week by year
        week += 53 * (this_time[0] - first_year)

        # Construct data structure in riwayat_ketepatan
        riwayat_ketepatan[week] = riwayat_ketepatan.get(week, this_weeks_laporan[True])

        # Check is punctual
        is_punctual = (one_laporan.waktu_deadline != none_check) and (one_laporan.waktu_submisi != none_check)
        is_punctual = is_punctual and (one_laporan.waktu_deadline >= one_laporan.waktu_submisi)
        this_weeks_laporan[is_punctual] += 1

        # Add to riwayat_ketepatan
        riwayat_ketepatan[week] += this_weeks_laporan[True]

        # Add to total_pengumpulan
        this_week_total_submission = (this_weeks_laporan[True] + this_weeks_laporan[False])
        total_pengumpulan[week] = total_pengumpulan.get(week, 0) + this_week_total_submission

    # By default, add this week's data as 0
    today_time = datetime.datetime.now()
    today_week = datetime.date(today_time.year, today_time.month, today_time.day).isocalendar()[1]

    today_week -= first_week - 1
    riwayat_ketepatan[today_week] = riwayat_ketepatan.get(today_week, 0)

    # Remove week 0
    riwayat_ketepatan.pop(0, None)
    total_pengumpulan.pop(0, None)

    return {"first_week": first_week, "riwayat_ketepatan": riwayat_ketepatan, "total_pengumpulan": total_pengumpulan}


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get_riwayat_ketepatan_pengumpulan(request):
    '''
    API Endpoint:
        http://localhost:8000/api/v1/koordinator-kuliah/riwayat-ketepatan-pengumpulan-laporan

    Expected output:
        Weekly Count of Puctually submitted report

    Output Format:
        success: boolean
        status_code: html status code
        data: JSON Data
    '''

    try:
        riwayat_ketepatan = get_ketepatan_pengumpulan_per_week()['riwayat_ketepatan']

        status_code = status.HTTP_200_OK
        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: 'Riwayat Ketepatan Pengumpulan Laporan fetched successfully',
            'data': riwayat_ketepatan,
            'count': len(riwayat_ketepatan.keys()),
        }

    # [ Exception Handling ]
    except KelolaLaporanPraktikum.DoesNotExist:
        # To indicate that KelolaLaporanPraktikum is not found and give clear info about the problem
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Laporan Praktikum cannot be found',
            'data': [],
            'count': 0,
        }

    except TypeError:
        # To indicate that the data type that is used is validto be compared with ">" operator
        # waktu_deadline and waktu_submisi should be in the type of DateTime
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Invalid data type exist in database',
            'data': [],
            'count': 0,
        }

    except UnicodeDecodeError:
        # To indicate that the server failed to read unicode or special characters
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Failed to read unicode characters',
            'data': [],
            'count': 0,
        }

    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get_persentase_ketepatan_pengumpulan(request):
    '''
    API Endpoint:
        http://localhost:8000/api/v1/koordinator-kuliah/persentase-ketepatan-pengumpulan-laporan

    Expected output:
        Weekly Percentage of Puctually submitted report
        and The comparison to the previous week

    Output Format:
        success: boolean
        status_code: html status code
        data: JSON Data
    '''
    output = {"this_week": 0, "previous_week": 0}
    try:
        riwayat = get_ketepatan_pengumpulan_per_week()

        today_time = datetime.datetime.now()
        today_time = datetime.date(today_time.year, today_time.month, today_time.day).isocalendar()
        this_week = today_time[1]

        this_week -= riwayat['first_week'] - 1

        last_week = this_week - 1

        ketepatan_this_week = riwayat['riwayat_ketepatan'].get(this_week, 0)
        total_this_week = riwayat['total_pengumpulan'].get(this_week, 1)

        ketepatan_last_week = riwayat['riwayat_ketepatan'].get(last_week, 0)
        total_last_week = riwayat['total_pengumpulan'].get(last_week, 1)

        last_percentage = round(ketepatan_this_week * 100 / total_this_week, 2)
        second_last_percentage = round(ketepatan_last_week * 100 / total_last_week, 2)

        difference = (ketepatan_this_week - ketepatan_last_week) * 100 / max(1, ketepatan_last_week)
        difference = round(difference, 2)

        status_code = status.HTTP_200_OK
        output["this_week"] = last_percentage
        output["previous_week"] = second_last_percentage
        output["difference_percent"] = difference

        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: 'Persentase Ketepatan Pengumpulan Laporan calculated successfully',
            'data': output,
        }

    # [ Exception Handling ]
    except KelolaLaporanPraktikum.DoesNotExist:
        # To indicate that KelolaLaporanPraktikum is not found and give clear info about the problem
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'No Laporan Praktikum Mingguan found!',
            'data': output,
        }

    except TypeError:
        # To indicate that the data type that is used is validto be compared with ">" operator
        # waktu_deadline and waktu_submisi should be in the type of DateTime
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Invalid data type found in database',
            'data': output,
        }

    except UnicodeDecodeError:
        # To indicate that the server failed to read unicode or special characters
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Failed to read unicode characters!',
            'data': output,
        }

    return Response(response, status=status.HTTP_200_OK)


def get_penilaian_laporan_per_week():
    # Retrieve Laporan from Database
    laporan = KelolaLaporanPraktikum.objects.filter(status_publikasi=True).order_by('waktu_deadline')
    # laporan_dinilai and total_pengumpulan are for output
    laporan_dinilai = dict()
    total_laporan = dict()

    # First Week of the first submission
    one_laporan = laporan[0:1].get()
    first_time = datetime.date(one_laporan.waktu_deadline.year, one_laporan.waktu_deadline.month, one_laporan.waktu_deadline.day).isocalendar()
    first_week = first_time[1]

    # First Year
    first_year = datetime.date(one_laporan.waktu_deadline.year, one_laporan.waktu_deadline.month, one_laporan.waktu_deadline.day).isocalendar()[0]

    # Iterate Through Laporan
    for one_laporan in laporan:
        # Skip if Mahasiswa is not active anymore
        is_active = KelolaLaporanPraktikum.objects.filter(mahasiswa=one_laporan.mahasiswa, status_publikasi=True).count() > 0
        if not is_active:
            continue

        # Dictionary for counting this week's submission time
        this_weeks_laporan = {}
        this_weeks_laporan[True] = 0
        this_weeks_laporan[False] = 0

        # Get Week
        this_time = datetime.date(one_laporan.waktu_deadline.year, one_laporan.waktu_deadline.month, one_laporan.waktu_deadline.day).isocalendar()
        week = this_time[1]

        # Adjust week according to first week
        week = week - first_week + 1

        # Adjust week by year
        week += 53 * (this_time[0] - first_year)

        # Construct data structure in laporan_dinilai
        laporan_dinilai[week] = laporan_dinilai.get(week, this_weeks_laporan[True])

        # Check is graded
        is_graded = (one_laporan.skor_laporan_sekolah >= 0)
        this_weeks_laporan[is_graded] += 1

        # Add to laporan_dinilai
        laporan_dinilai[week] += this_weeks_laporan[True]

        # Add to total_laporan
        this_week_total_submission = (this_weeks_laporan[True] + this_weeks_laporan[False])
        total_laporan[week] = total_laporan.get(week, 0) + this_week_total_submission

    # By default, add this week's data as 0
    today_time = datetime.datetime.now()
    today_week = datetime.date(today_time.year, today_time.month, today_time.day).isocalendar()[1]
    today_week -= first_week - 1
    laporan_dinilai[today_week] = laporan_dinilai.get(today_week, 0)

    return {"first_week": first_week, "laporan_dinilai": laporan_dinilai, "total_laporan": total_laporan}


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get_persentase_penilaian_laporan_supervisor_sekolah(request):
    '''
    API Endpoint:
        http://localhost:8000/api/v1/koordinator-kuliah/persentase-penilaian-laporan-supervisor-sekolah

    Expected output:
        Weekly Percentage of Puctually submitted report
        and The comparison to the previous week

    Output Format:
        success: boolean
        status_code: html status code
        data: JSON Data
    '''
    output = {"this_week": 0, "previous_week": 0}
    try:
        riwayat = get_penilaian_laporan_per_week()

        today_time = datetime.datetime.now()
        today_time = datetime.date(today_time.year, today_time.month, today_time.day).isocalendar()
        this_week = today_time[1]

        this_week -= riwayat['first_week'] - 1

        last_week = this_week - 1

        laporan_dinilai_this_week = riwayat['laporan_dinilai'].get(this_week, 0)
        total_laporan_this_week = riwayat['total_laporan'].get(this_week, 1)

        laporan_dinilai_last_week = riwayat['laporan_dinilai'].get(last_week, 0)
        total_laporan_last_week = riwayat['total_laporan'].get(last_week, 1)

        last_percentage = round(laporan_dinilai_this_week * 100 / total_laporan_this_week, 2)
        second_last_percentage = round(laporan_dinilai_last_week * 100 / total_laporan_last_week, 2)

        difference = (laporan_dinilai_this_week - laporan_dinilai_last_week) * 100 / max(1, laporan_dinilai_last_week)
        difference = round(difference, 2)

        status_code = status.HTTP_200_OK
        output["this_week"] = last_percentage
        output["previous_week"] = second_last_percentage
        output["difference_percent"] = difference

        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: 'Persentase penilaian Laporan has been calculated successfully',
            'data': output,
        }

    # [ Exception Handling ]
    except KelolaLaporanPraktikum.DoesNotExist:
        # To indicate that KelolaLaporanPraktikum is not found and give clear info about the problem
        status_code = status.HTTP_404_NOT_FOUND
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'No Laporan Praktikum Mingguan found.',
            'data': output,
        }

    except TypeError:
        # To indicate that the data type that is used is validto be compared with ">" operator
        # waktu_deadline and waktu_submisi should be in the type of DateTime
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Invalid data type found in database.',
            'data': output,
        }

    except UnicodeDecodeError:
        # To indicate that the server failed to read unicode or special characters
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Failed to read unicode characters.',
            'data': output,
        }

    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_statistik_lembaga(request):
    '''
    API Endpoint:
        http://localhost:8000/api/v1/statistik-lembaga

    Expected output:
        Statistik Lembaga, filtered by tema/institusi & Year
    '''
    result = dict()

    try:
        lembaga = Lembaga.objects.all()

        # Institusi
        institusi = Institusi.objects.all()
        institusi = [i.nama for i in institusi]

        # Tema
        tema = Tema.objects.all()
        tema = [i.nama for i in tema]

        if request.GET['berdasarkan'] == "institusi":
            lembaga = lembaga.filter(institusi__nama__in=institusi)
            for i in lembaga:
                nama_institusi = i.institusi.nama
                result[nama_institusi] = result.get(nama_institusi, 0) + 1
        else:
            lembaga = lembaga.filter(institusi__nama__in=tema)
            for i in lembaga:
                nama_tema = i.tema.nama
                result[nama_tema] = result.get(nama_tema, 0) + 1

        status_code = status.HTTP_200_OK
        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: 'Statistik Lembaga has been loaded successfully',
            'data': result,
        }

    # [ Exception Handling ]
    except KeyError:
        # To indicate that KelolaLaporanPraktikum is not found and give clear info about the problem
        status_code = status.HTTP_400_BAD_REQUEST
        response = {
            response_field[0]: 'False',
            response_field[1]: status_code,
            response_field[2]: 'Please set the filter',
            'data': result,
        }

    return Response(response, status=status_code)
