from authentication.models import (
    User,
    Mahasiswa,
    SupervisorLembaga,
    KoordinatorKuliah,
    SupervisorSekolah,
    Administrator,
    Periode
)
from laporan_praktikum.models import (
    Praktikum,
    KelolaLaporanPraktikum,
    MahasiswaPraktikum
)
from laporan_praktikum.serializers import (
    RiwayatLaporanPraktikumMahasiswaSerializer
)
from lembaga.models import Lembaga, Tema, Institusi
from laporan_praktikum.models import LaporanAkhirPraktikum

from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework_jwt.settings import api_settings
from django.urls import reverse
from mixer.backend.django import mixer
from io import BytesIO
from PIL import Image
from django.core.files import File
from rest_framework import status

import collections
import datetime
import json

factory = APIRequestFactory()
request = factory.get('/')

serializer_context = {
    'request': Request(request),
}

response_field = ['success', 'status_code', 'message']
token_type = "Bearer "
'''
class RiwayatLaporanPraktikumLembagaTest(TestCase):
    
    def setUp(self):

        jenis_praktikum = Praktikum.objects.create(
            jenis_praktikum="Praktikum 1"
        )

        user_mahasiswa = User.objects.create_user(
            username="username1",
            role=Role.MHS.value,
            email="username1@email.com",
            password="password",
            full_name="User Name1"
        )

        lembaga_test = Lembaga.objects.create(nama="nama_lembaga_4")
        lembaga_test.save()

        laporan = LaporanAkhirPraktikum.objects.create(
            mahasiswa = user_mahasiswa,
            jenis_praktikum = jenis_praktikum,
            lembaga = Lembaga.objects.get(nama="nama_lembaga_4"),
            praktikum_ke = 1,
            periode_praktikum = "",
            laporan_akhir = "",
            profil_lembaga = "",
            umpan_balik = "",
        )

    def test_get_riwayat_laporan_exist(self):
        laporan_mahasiswa = LaporanAkhirPraktikum.objects.filter(lembaga=Lembaga.objects.get(nama="nama_lembaga_4").id)
        self.assertNotEqual(laporan_mahasiswa, [])

    def test_get_riwayat_laporan_empty_string(self):
        laporan_mahasiswa = LaporanAkhirPraktikum.objects.filter(lembaga=Lembaga.objects.get(nama="").id).count()
        self.assertFalse(laporan_mahasiswa, [])

'''
class TestListMahasiswaSupervisorLembaga(APITestCase):
    def setUp(self):
        self.JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
        self.JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

        self.user_supervisor_lembaga = User.objects.create_user(
            username="username3",
            email="username3@email.com",
            password="password",
            first_name="User",
            last_name="Name3"
        )

        
    def test_no_mahasiswa_for_supervisor_lembaga(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_supervisor_lembaga)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)

        response = self.client.get(
            reverse('laporan_praktikum:supervisor-lembaga-list-mahasiswa'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_see_API_without_login(self):
        response = self.client.get(
            reverse('laporan_praktikum:supervisor-lembaga-list-mahasiswa'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RiwayatLaporanPraktikumMahasiswaTest(TestCase):

    def setUp(self):

        jenis_praktikum = Praktikum.objects.create(
            jenis_praktikum="Praktikum 1"
        )

        user_mahasiswa = User.objects.create_user(
            username="username1",
            email="username1@email.com",
            password="password",
            first_name="User",
            last_name="Name1"
        )

        user_mahasiswa_2 = User.objects.create_user(
            username="username2",
            email="username2@email.com",
            password="password",
            first_name="User",
            last_name="Name2"
        )

        self.user_mahasiswa_3 = User.objects.create_user(
            username="username3",
            email="username1@email.com",
            password="password",
            first_name="User",
            last_name="Name1"
        )

        periode = Periode.objects.create(
            nama="periode"
        )

        profile_mahasiswa = Mahasiswa.objects.create(
            user=user_mahasiswa,
            npm="npm",
            org_code="org_code",
            faculty="faculty",
            major="major",
            program="program",
            periode=periode,
            supervisor_lembaga=None,
            supervisor_sekolah=None
        )

        profile_mahasiswa_2 = Mahasiswa.objects.create(
            user=user_mahasiswa_2,
            npm="npm",
            org_code="org_code",
            faculty="faculty",
            major="major",
            program="program",
            periode=periode,
            supervisor_lembaga=None,
            supervisor_sekolah=None
        )

        self.profile_mahasiswa_3 = Mahasiswa.objects.create(
            user=self.user_mahasiswa_3,
            npm="npm",
            org_code="org_code",
            faculty="faculty",
            major="major",
            program="program",
            periode=periode,
            supervisor_lembaga=None,
            supervisor_sekolah=None
        )

        laporan_praktikum = KelolaLaporanPraktikum.objects.create(
            nama_laporan="Laporan Minggu 1",
            waktu_deadline=datetime.datetime.now(),
            waktu_submisi=None,
            status_publikasi=True,
            status_submisi=False,
            skor_laporan_sekolah=-1,
            skor_laporan_lembaga=-1,
            mahasiswa=profile_mahasiswa,
            jenis_praktikum=jenis_praktikum,
            link_submisi="http://website.hosted/laporan_minggu1.pdf"
        )

        laporan_praktikum_for_xss = KelolaLaporanPraktikum.objects.create(
            nama_laporan="Laporan Minggu 2",
            waktu_deadline=datetime.datetime.strptime("12-12-9999 23:54", '%d-%m-%Y %H:%M'),
            waktu_submisi=None,
            status_publikasi=True,
            status_submisi=False,
            skor_laporan_sekolah=-1,
            skor_laporan_lembaga=-1,
            mahasiswa=self.profile_mahasiswa_3,
            jenis_praktikum=jenis_praktikum,
            link_submisi=None
        )

    def test_get_riwayat_laporan_by_mahasiswa(self):
        user_mahasiswa_data = User.objects.get(username="username1")
        profile_mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa_data)
        laporan_mahasiswa = KelolaLaporanPraktikum.objects.filter(mahasiswa=profile_mahasiswa)
        serializer = RiwayatLaporanPraktikumMahasiswaSerializer(laporan_mahasiswa, context=serializer_context, many=True)
        self.assertNotEqual(laporan_mahasiswa.count(), 0)
        self.assertNotEqual(serializer.data, [])

    def test_get_riwayat_laporan_by_mahasiswa_empty(self):
        user_mahasiswa_data = User.objects.get(username="username2")
        profile_mahasiswa = Mahasiswa.objects.get(user=user_mahasiswa_data)
        laporan_mahasiswa = KelolaLaporanPraktikum.objects.filter(mahasiswa=profile_mahasiswa)
        serializer = RiwayatLaporanPraktikumMahasiswaSerializer(laporan_mahasiswa, context=serializer_context, many=True)
        self.assertEqual(laporan_mahasiswa.count(), 0)
        self.assertEqual(serializer.data, [])

    def test_post_invalid_laporan_by_mahasiswa(self):
        payload = api_settings.JWT_PAYLOAD_HANDLER(self.user_mahasiswa_3)
        jwt_token = api_settings.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        laporan_id = KelolaLaporanPraktikum.objects.get(nama_laporan="Laporan Minggu 2").id
        response = client.post(reverse('laporan_praktikum:submit-link-laporan-praktikum'), {'id':laporan_id,'waktu_submisi':"12-12-2020 23:54",'link_submisi':'javascript:alert(1)','status_submisi':True})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_post_valid_laporan_by_mahasiswa(self):
        payload = api_settings.JWT_PAYLOAD_HANDLER(self.user_mahasiswa_3)
        jwt_token = api_settings.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        laporan_id = KelolaLaporanPraktikum.objects.get(nama_laporan="Laporan Minggu 2").id
        response = client.post(reverse('laporan_praktikum:submit-link-laporan-praktikum'), {'id':laporan_id,'waktu_submisi':"12-12-2020 23:54",'link_submisi':'http://evil.com','status_submisi':True})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class MahasiswaAPITest(TestCase):
    def setUp(self):
        periode = Periode.objects.create(
            nama="periode"
        )

        user_mahasiswa = User.objects.create_user(
            username="username1",
            email="username1@email.com",
            password="password",
            first_name="User",
            last_name="Name1"
        )

        user_mahasiswa_2 = User.objects.create_user(
            username="username2",
            email="username2@email.com",
            password="password",
            first_name="User",
            last_name="Name2"
        )

        profile_mahasiswa = Mahasiswa.objects.create(
            user=user_mahasiswa,
            npm="1806243684",
            org_code="org_code",
            faculty="faculty",
            major="major",
            program="program",
            periode=periode,
            supervisor_lembaga=None,
            supervisor_sekolah=None
        )

        profile_mahasiswa_2 = Mahasiswa.objects.create(
            user=user_mahasiswa_2,
            npm="1806241085",
            org_code="org_code",
            faculty="faculty",
            major="major",
            program="program",
            periode=periode,
            supervisor_lembaga=None,
            supervisor_sekolah=None
        )

    # Test to check whether the API Load all mahasiswa Data
    def test_get_all_mahasiswa(self):
        data = Mahasiswa.objects.all()
        # Test if it returns non empty data
        self.assertTrue(len(data) > 0)

    # Test to check whether the API can filter data by npm (EXISTS)
    def test_get_mahasiswa_by_npm_exists(self):
        data = Mahasiswa.objects.filter(npm=1806241085)
        self.assertTrue(len(data) > 0)

    # Test to check whether the API can filter data by npm (NOT EXISTS)
    def test_get_mahasiswa_by_npm_not_exists(self):
        data = Mahasiswa.objects.filter(npm=180624108500)
        self.assertTrue(len(data) == 0)

    # Test to check whether the API can handle NULL input or not
    def test_get_mahasiswa_by_npm_null(self):
        data = Mahasiswa.objects.filter(npm=None)
        self.assertTrue(len(data) == 0)

    # Test API can be loaded
    def test_can_see_API(self):
        response = self.client.get(
            reverse('laporan_praktikum:mahasiswa'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PeriodeAPITest(APITestCase):
    """
    Test for supervisor sekolah list and detail laporan
    """
    def get_image_file(self, name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        '''Mock image'''
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        self.JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
        self.JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

        self.user_mahasiswa_not_valid2 = User.objects.create_user(
            username="username1",
            email="username1@email.com",
            password="password",
            first_name="User",
            last_name="Name1"
        )

        self.user_mahasiswa = User.objects.create_user(
            username="username2",
            email="username2@email.com",
            password="password",
            first_name="User",
            last_name="Name2"
        )

        self.supervisor_sekolah = mixer.blend(
            SupervisorSekolah, user=mixer.blend(
                User
            )
        )

        self.supervisor_lembaga = mixer.blend(
            SupervisorLembaga, lembaga=mixer.blend(
                Lembaga, institusi=mixer.blend(
                    Institusi
                ), tema=mixer.blend(
                    Tema
                ), gambar=self.get_image_file()
            ), user=mixer.blend(
                User
            )
        )

        periode = Periode.objects.create(
            nama="periode"
        )

        self.mahasiswa = mixer.blend(
            Mahasiswa,
            supervisor_lembaga=self.supervisor_lembaga,
            supervisor_sekolah=self.supervisor_sekolah,
            periode=periode,
            user=self.user_mahasiswa
        )

        Mahasiswa.objects.create(
            user=self.user_mahasiswa_not_valid2,
            npm="npm",
            org_code="org_code",
            faculty="faculty",
            major="major",
            program="program",
            periode=periode,
            supervisor_lembaga=self.supervisor_lembaga,
            supervisor_sekolah=self.supervisor_sekolah
        )

        self.user_koordinator_kuliah = User.objects.create_user(
            username="username3",
            email="username3@email.com",
            password="password",
            first_name="User",
            last_name="Name3"
        )

        koordinator_kuliah = KoordinatorKuliah.objects.create(
            user=self.user_koordinator_kuliah,
            nip="nip"
        )

        praktikum = Praktikum.objects.create(
            jenis_praktikum="Praktikum 1"
        )

        MahasiswaPraktikum.objects.create(
            mahasiswa=self.mahasiswa,
            list_praktikum=praktikum,
            status=True
        )

        KelolaLaporanPraktikum.objects.create(
            nama_laporan='nama_laporan_1',
            mahasiswa=self.mahasiswa,
            jenis_praktikum=praktikum,
            waktu_deadline=datetime.datetime(
                2020,
                5,
                5,
                5,
                5,
                5
            ),
            status_publikasi=True,
            status_submisi=False,
            skor_laporan_sekolah=-1,
            skor_laporan_lembaga=-1
        )
  
    def test_can_load_api(self):
        response = self.client.get(
            reverse('laporan_praktikum:periode'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class KoordinatorKuliahDashboardAPITest(APITestCase):
    """
    Test for supervisor sekolah list and detail laporan
    """
    def get_image_file(self, name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        '''Mock image'''
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        self.JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
        self.JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

        self.user_mahasiswa_not_valid2 = User.objects.create_user(
            username="username1",
            email="username1@email.com",
            password="password",
            first_name="User",
            last_name="Name1"
        )

        self.user_mahasiswa = User.objects.create_user(
            username="username2",
            email="username2@email.com",
            password="password",
            first_name="User",
            last_name="Name2"
        )

        self.supervisor_sekolah = mixer.blend(
            SupervisorSekolah, user=mixer.blend(
                User
            )
        )

        self.supervisor_lembaga = mixer.blend(
            SupervisorLembaga, lembaga=mixer.blend(
                Lembaga, institusi=mixer.blend(
                    Institusi
                ), tema=mixer.blend(
                    Tema
                ), gambar=self.get_image_file()
            ), user=mixer.blend(
                User
            )
        )

        periode = Periode.objects.create(
            nama="periode"
        )

        self.mahasiswa = mixer.blend(
            Mahasiswa,
            supervisor_lembaga=self.supervisor_lembaga,
            supervisor_sekolah=self.supervisor_sekolah,
            periode=periode,
            user=self.user_mahasiswa
        )

        Mahasiswa.objects.create(
            user=self.user_mahasiswa_not_valid2,
            npm="npm",
            org_code="org_code",
            faculty="faculty",
            major="major",
            program="program",
            periode=periode,
            supervisor_lembaga=self.supervisor_lembaga,
            supervisor_sekolah=self.supervisor_sekolah
        )

        self.user_koordinator_kuliah = User.objects.create_user(
            username="username3",
            email="username3@email.com",
            password="password",
            first_name="User",
            last_name="Name3"
        )

        koordinator_kuliah = KoordinatorKuliah.objects.create(
            user=self.user_koordinator_kuliah,
            nip="nip"
        )

        praktikum = Praktikum.objects.create(
            jenis_praktikum="Praktikum 1"
        )

        MahasiswaPraktikum.objects.create(
            mahasiswa=self.mahasiswa,
            list_praktikum=praktikum,
            status=True
        )

        KelolaLaporanPraktikum.objects.create(
            nama_laporan='nama_laporan_1',
            mahasiswa=self.mahasiswa,
            jenis_praktikum=praktikum,
            waktu_deadline=datetime.datetime(
                2020,
                5,
                5,
                5,
                5,
                5
            ),
            status_publikasi=True,
            status_submisi=False,
            skor_laporan_sekolah=-1,
            skor_laporan_lembaga=-1
        )

    # Koordinator Kuliah Mahasiswa List    
    def test_can_not_see_list_mahasiswa_koordinator_kuliah_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=token_type + 'falsetoken')
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-list-mahasiswa'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_list_mahasiswa_other_role_in_login_koordinator_kuliah(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.mahasiswa.user)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-list-mahasiswa'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Koordinator Kuliah Daftar Mahasiswa
    def test_can_see_daftar_mahasiswa_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        # Test API URL is accessible without parameter
        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:mahasiswa', kwargs={}))
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

        # Test API URL is accessible with npm parameter
        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            "%s?npm=npm" % reverse('laporan_praktikum:mahasiswa'))
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    # Koordinator Kuliah Grafik Pengumpulan
    # [ Negative Test ]
    # seeing API without login and no authorization token
    '''def test_can_see_grafik_pengumpulan_tepat_waktu_without_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        # Test API URL without providing AUTH TOKEN
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-grafik-pengumpulan-tepat-waktu'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)'''

    # [ Positive Tests ]
    # seeing API after login and with authorization token
    def test_can_see_grafik_pengumpulan_tepat_waktu_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        # Test API URL is accessible (Normal Flow)
        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-grafik-pengumpulan-tepat-waktu'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Check if the API can load all the data
    def test_can_load_data(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token
        
        # Test API URL is accessible (Normal Flow)
        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-grafik-pengumpulan-tepat-waktu'))
        self.assertIsNotNone(response.content)

    # ====================================================
    # Koordinator Kuliah Persentase Ketepatan Pengumpulan
    # ====================================================
    # [ Negative Test ]
    # seeing API without login and no authorization token
    '''def test_can_see_persentase_ketepatan_pengumpulan_without_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        # Test API URL without providing AUTH TOKEN
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-persentase-pengumpulan-laporan'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)'''

    # [ Positive Tests ]
    # seeing API after login and with authorization token
    def test_can_see_persentase_ketepatan_pengumpulan_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        # Test API URL is accessible (Normal Flow)
        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-persentase-pengumpulan-laporan'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Check if the API can load all the data
    def test_can_load_data_persentase_ketepatan_pengumpulan(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token
        
        # Test API URL is accessible (Normal Flow)
        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-persentase-pengumpulan-laporan'))
        self.assertIsNotNone(response.content)

    # ====================================================
    # Koordinator Kuliah Persentase Penilaian
    # ====================================================
    # [ Negative Test ]
    # seeing API without login and no authorization token
    '''def test_can_see_persentase_ketepatan_pengumpulan_without_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        # Test API URL without providing AUTH TOKEN
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-persentase-penilaian-laporan'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)'''

    # [ Positive Tests ]
    # seeing API after login and with authorization token
    def test_can_see_persentase_penilaian_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        # Test API URL is accessible (Normal Flow)
        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-persentase-penilaian-laporan'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Check if the API can load all the data
    def test_can_load_data_persentase_penilaian(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token
        
        # Test API URL is accessible (Normal Flow)
        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-persentase-penilaian-laporan'))
        self.assertIsNotNone(response.content)

    # ======================================================================================
    # Koordinator Kuliah Laporan List
    def test_can_see_list_laporan_koordinator_kuliah_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-persentase-pengumpulan-laporan'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_list_laporan_koordinator_kuliah_because_of_no_user(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-list-praktikum-mahasiswa', kwargs={'username': 'usernamefake'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_list_laporan_koordinator_kuliah_because_of_no_praktikum(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-list-praktikum-mahasiswa', kwargs={'username': 'username1'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_list_laporan_koordinator_kuliah_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=token_type + 'falsetoken')
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-list-praktikum-mahasiswa', kwargs={'username': 'username2'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_list_laporan_other_role_in_login_koordinator_kuliah(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_mahasiswa)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-list-praktikum-mahasiswa', kwargs={'username': 'username3'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Koordinator Kuliah Detail List

    def test_can_see_detail_laporan_koordinator_kuliah_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-detail-laporan-mingguan-mahasiswa', kwargs={'username': 'username2', 'id': '1'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_detail_laporan_koordinator_kuliah_because_of_no_user(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-detail-laporan-mingguan-mahasiswa', kwargs={'username': 'usernamefake', 'id': '1'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_detail_laporan_koordinator_kuliah_because_of_no_laporan(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-detail-laporan-mingguan-mahasiswa', kwargs={'username': 'username2', 'id': '2'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_detail_laporan_koordinator_kuliah_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=token_type + 'falsetoken')
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-detail-laporan-mingguan-mahasiswa', kwargs={'username': 'username2', 'id': '1'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_detail_laporan_other_role_in_login_koordinator_kuliah(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_mahasiswa)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:koordinator-kuliah-detail-laporan-mingguan-mahasiswa', kwargs={'username': 'username3', 'id': '1'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AdministratorDashboardAPITest(APITestCase):
    """
    Test for administrator
    """

    def setUp(self):
        self.JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
        self.JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

        self.user_administrator = User.objects.create_user(
            username="username4",
            email="username4@email.com",
            password="password",
            first_name="User",
            last_name="Name4"
        )

        administrator = Administrator.objects.create(
            user=self.user_administrator,
            nip="nip"
        )

        self.user_koordinator_kuliah = User.objects.create_user(
            username="username3",
            email="username3@email.com",
            password="password",
            first_name="User",
            last_name="Name3"
        )

        self.koordinator_kuliah = mixer.blend(
            KoordinatorKuliah,
            user=self.user_koordinator_kuliah
        )

        self.supervisor_sekolah = mixer.blend(
            SupervisorSekolah,
            user=mixer.blend(
                User,
                username="username1"
            )
        )

        self.supervisor_lembaga = mixer.blend(
            SupervisorLembaga, lembaga=mixer.blend(
                Lembaga, institusi=mixer.blend(
                    Institusi
                ), tema=mixer.blend(
                    Tema
                ), 
            ), user=mixer.blend(
                User,
                username="username2",
            )
        )
        
        self.mahasiswa = mixer.blend(
            Mahasiswa,
            supervisor_lembaga=self.supervisor_lembaga,
            supervisor_sekolah=self.supervisor_sekolah,
            user=mixer.blend(
                User,
                username="username0",
                email="username0@email.com",
            )
        )

        praktikum = Praktikum.objects.create(
            jenis_praktikum="Praktikum 1"
        )

        MahasiswaPraktikum.objects.create(
            mahasiswa=self.mahasiswa,
            list_praktikum=praktikum,
            status=True
        )
    
       # [ Administrator Statistik ]

    # =================
    # [ Positive Test ] 
    # =================
    def test_can_see_statistik_administrator_by_tema_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get('/api/v1/administrator/statistik-lembaga?berdasarkan=tema&tahun=2020')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_see_statistik_administrator_by_institusi_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get('/api/v1/administrator/statistik-lembaga?berdasarkan=institusi&tahun=2020')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # =================
    # [ Negative Test ]
    # =================
    def test_can_not_see_statistik_administrator_before_login(self):
            # Provide False Token
        self.client.credentials(HTTP_AUTHORIZATION=token_type + 'falsetoken')
        response = self.client.get('/api/v1/administrator/statistik-lembaga?berdasarkan=tema&tahun=2020')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_statistik_administrator_without_parameters(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-statistik'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Administrator User List

    def test_can_see_list_user_administrator_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-list-user'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_can_not_see_list_user_administrator_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=token_type + 'falsetoken')
        response = self.client.get(
            reverse('laporan_praktikum:administrator-list-user'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_list_user_other_role_in_login_administrator(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-list-user'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Administrator Detail Kelola Mahasiswa

    def test_can_see_detail_kelola_mahasiswa_data_by_administrator_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-mahasiswa', kwargs={'username': 'username0'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_detail_kelola_mahasiswa_data_by_administrator_because_of_no_user(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-mahasiswa', kwargs={'username': 'usernamefake'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_detail_kelola_mahasiswa_data_by_administrator_because_of_not_mahasiswa(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-mahasiswa', kwargs={'username': 'username1'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_detail_kelola_mahasiswa_data_by_administrator_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=token_type + 'falsetoken')
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-mahasiswa', kwargs={'username': 'username0'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_detail_kelola_other_role_for_mahasiswa_in_login_administrator(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-mahasiswa', kwargs={'username': 'username0'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Administrator Detail Kelola Supervisor Sekolah

    def test_can_see_detail_kelola_supervisor_sekolah_data_by_administrator_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-supervisor-sekolah', kwargs={'username': 'username1'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_detail_kelola_supervisor_sekolah_data_by_administrator_because_of_no_user(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-supervisor-sekolah', kwargs={'username': 'usernamefake'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_detail_kelola_supervisor_sekolah_data_by_administrator_because_of_not_supervisor_sekolah(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-supervisor-sekolah', kwargs={'username': 'username2'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_detail_kelola_supervisor_sekolah_data_by_administrator_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=token_type + 'falsetoken')
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-supervisor-sekolah', kwargs={'username': 'username1'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_detail_kelola_other_role_for_supervisor_sekolah_in_login_administrator(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-supervisor-sekolah', kwargs={'username': 'username1'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Administrator Detail Kelola Supervisor Lembaga

    def test_can_see_detail_kelola_supervisor_lembaga_data_by_administrator_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-supervisor-lembaga', kwargs={'username': 'username2'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_detail_kelola_supervisor_lembaga_data_by_administrator_because_of_no_user(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-supervisor-lembaga', kwargs={'username': 'usernamefake'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_detail_kelola_supervisor_lembaga_data_by_administrator_because_of_not_supervisor_lembaga(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-supervisor-lembaga', kwargs={'username': 'username3'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_detail_kelola_supervisor_lembaga_data_by_administrator_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=token_type + 'falsetoken')
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-supervisor-lembaga', kwargs={'username': 'username2'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_detail_kelola_other_role_for_supervisor_lembaga_in_login_administrator(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-supervisor-lembaga', kwargs={'username': 'username2'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Administrator Detail Kelola Koordinator Kuliah

    def test_can_see_detail_kelola_koordinator_kuliah_data_by_administrator_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-koordinator-kuliah', kwargs={'username': 'username3'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_detail_kelola_koordinator_kuliah_data_by_administrator_because_of_no_user(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-koordinator-kuliah', kwargs={'username': 'usernamefake'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_detail_kelola_koordinator_kuliah_data_by_administrator_because_of_not_koordinator_kuliah(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-koordinator-kuliah', kwargs={'username': 'username4'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_detail_kelola_koordinator_kuliah_data_by_administrator_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=token_type + 'falsetoken')
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-koordinator-kuliah', kwargs={'username': 'username3'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_detail_kelola_other_role_for_koordinator_kuliah_in_login_administrator(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-koordinator-kuliah', kwargs={'username': 'username3'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

   # Administrator Detail Kelola Administrator

    def test_can_see_detail_kelola_administrator_data_by_administrator_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-administrator', kwargs={'username': 'username4'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_detail_kelola_administrator_data_by_administrator_because_of_no_user(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-administrator', kwargs={'username': 'usernamefake'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_detail_kelola_administrator_data_by_administrator_because_of_not_administrator(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-administrator', kwargs={'username': 'username0'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_detail_kelola_administrator_data_by_administrator_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=token_type + 'falsetoken')
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-administrator', kwargs={'username': 'username4'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_detail_kelola_other_role_for_administrator_in_login_administrator(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:administrator-detail-user-administrator', kwargs={'username': 'username4'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

