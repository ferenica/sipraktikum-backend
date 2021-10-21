from laporan_praktikum.models import Praktikum, KelolaLaporanPraktikum, MahasiswaPraktikum
from authentication.models import Mahasiswa, SupervisorLembaga, SupervisorSekolah, User, Periode
from lembaga.models import Lembaga, Tema, Institusi
from django.test import TestCase
from django.core.files import File
from io import BytesIO
from rest_framework.test import APITestCase
from rest_framework import serializers
from rest_framework import status
from PIL import Image
import json
import datetime
from rest_framework_jwt.settings import api_settings
from django.urls import reverse
from mixer.backend.django import mixer

'''
TODO: Unit Test Kelola Laporan Praktikum
'''
class ModelsTest(TestCase):

    def setUp(self):
        Praktikum.objects.create(jenis_praktikum='Laporan Minggu 1')

    def test_create_models_praktikum(self):
        jenis_praktikum = Praktikum.objects.get(jenis_praktikum='Laporan Minggu 1')
        self.assertEqual(type(jenis_praktikum.__str__()), str)



token_type = "Bearer "
class SupervisorSekolahDashboardAPITest(APITestCase):
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

        self.user_mahasiswa_not_valid1 = User.objects.create_user(
            username="username0",
            email="username0@email.com",
            password="password",
            first_name="User",
            last_name="Name0"
        )

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

        self.user_supervisor_sekolah = User.objects.create_user(
            username="username3",
            email="username3@email.com",
            password="password",
            first_name="User",
            last_name="Name3"
        )

        self.user_supervisor_lembaga = User.objects.create_user(
            username="username4",
            email="username4@email.com",
            password="password",
            first_name="User",
            last_name="Name4"
        )

        supervisor_lembaga = mixer.blend(
            SupervisorLembaga, lembaga=mixer.blend(
                Lembaga, institusi=mixer.blend(
                    Institusi
                ), tema=mixer.blend(
                    Tema
                ), gambar=self.get_image_file()
            ), user=mixer.blend(User)
        )

        supervisor_sekolah = SupervisorSekolah.objects.create(
            user=self.user_supervisor_sekolah,
            nip="nip"
        )

        periode = Periode.objects.create(
            nama="periode"
        )

        mahasiswa_not_valid_1 = Mahasiswa.objects.create(
            user=self.user_mahasiswa_not_valid1,
            npm="npm",
            org_code="org_code",
            faculty="faculty",
            major="major",
            program="program",
            periode=periode,
            supervisor_lembaga=supervisor_lembaga,
            supervisor_sekolah=supervisor_sekolah
        )

        Mahasiswa.objects.create(
            user=self.user_mahasiswa_not_valid2,
            npm="npm",
            org_code="org_code",
            faculty="faculty",
            major="major",
            program="program",
            periode=periode,
            supervisor_lembaga=supervisor_lembaga,
            supervisor_sekolah=supervisor_sekolah
        )

        mahasiswa = Mahasiswa.objects.create(
            user=self.user_mahasiswa,
            npm="npm",
            org_code="org_code",
            faculty="faculty",
            major="major",
            program="program",
            periode=periode,
            supervisor_lembaga=supervisor_lembaga,
            supervisor_sekolah=supervisor_sekolah
        )

        praktikum = Praktikum.objects.create(
            jenis_praktikum="Praktikum 1"
        )

        MahasiswaPraktikum.objects.create(
            mahasiswa=mahasiswa,
            list_praktikum=praktikum,
            status=True
        )

        MahasiswaPraktikum.objects.create(
            mahasiswa=mahasiswa_not_valid_1,
            list_praktikum=praktikum,
            status=True
        )

        KelolaLaporanPraktikum.objects.create(
            nama_laporan='nama_laporan_1',
            mahasiswa=mahasiswa,
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

        self.login_data_supervisor_sekolah_valid = {
            "username": "username3",
            "password": "password"
        }

    # Supervisor Sekolah Laporan List

    def test_can_see_list_laporan_supervisor_sekolah_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_supervisor_sekolah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:supervisor-sekolah-list-praktikum-mahasiswa', kwargs={'username': 'username2'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_list_laporan_supervisor_sekolah_because_of_no_user(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_supervisor_sekolah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:supervisor-sekolah-list-praktikum-mahasiswa', kwargs={'username': 'usernamefake'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_list_laporan_supervisor_sekolah_because_of_no_praktikum(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_supervisor_sekolah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:supervisor-sekolah-list-praktikum-mahasiswa', kwargs={'username': 'username1'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_list_laporan_supervisor_sekolah_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=token_type + 'falsetoken')
        response = self.client.get(
            reverse('laporan_praktikum:supervisor-sekolah-list-praktikum-mahasiswa', kwargs={'username': 'username2'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_list_laporan_other_role_in_login_supervisor_sekolah(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_mahasiswa)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:supervisor-sekolah-list-praktikum-mahasiswa', kwargs={'username': 'username3'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Supervisor Sekolah Detail List

    def test_can_see_detail_laporan_supervisor_sekolah_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_supervisor_sekolah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:supervisor-sekolah-detail-laporan-mingguan-mahasiswa', kwargs={'username': 'username2', 'id': '1'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_detail_laporan_supervisor_sekolah_because_of_no_user(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_supervisor_sekolah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:supervisor-sekolah-detail-laporan-mingguan-mahasiswa', kwargs={'username': 'usernamefake', 'id': '1'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_detail_laporan_supervisor_sekolah_because_of_no_laporan(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_supervisor_sekolah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:supervisor-sekolah-detail-laporan-mingguan-mahasiswa', kwargs={'username': 'username2', 'id': '2'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_see_detail_laporan_supervisor_sekolah_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=token_type + 'falsetoken')
        response = self.client.get(
            reverse('laporan_praktikum:supervisor-sekolah-detail-laporan-mingguan-mahasiswa', kwargs={'username': 'username2', 'id': '1'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_detail_laporan_other_role_in_login_supervisor_sekolah(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_mahasiswa)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.get(
            reverse('laporan_praktikum:supervisor-sekolah-detail-laporan-mingguan-mahasiswa', kwargs={'username': 'username3', 'id': '1'}), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Supervisor Sekolah Update Skor

    def test_can_update_skor_supervisor_sekolah_with_valid_skor_input(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_supervisor_sekolah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.put(
            reverse('laporan_praktikum:supervisor-sekolah-nilai-laporan-mingguan-mahasiswa',
            kwargs={'username': 'username2', 'id': '1'}),
            data={'format': 'json', 'skor': '50'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            reverse('laporan_praktikum:supervisor-sekolah-nilai-laporan-mingguan-mahasiswa',
            kwargs={'username': 'username2', 'id': '1'}),
            data={'format': 'json', 'skor': '0'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            reverse('laporan_praktikum:supervisor-sekolah-nilai-laporan-mingguan-mahasiswa',
            kwargs={'username': 'username2', 'id': '1'}),
            data={'format': 'json', 'skor': '100'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_update_skor_supervisor_sekolah_with_invalid_skor_input(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_supervisor_sekolah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.put(
            reverse('laporan_praktikum:supervisor-sekolah-nilai-laporan-mingguan-mahasiswa',
            kwargs={'username': 'username2', 'id': '1'}),
            data={'format': 'json', 'skor': '-2'}
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

        response = self.client.put(
            reverse('laporan_praktikum:supervisor-sekolah-nilai-laporan-mingguan-mahasiswa',
            kwargs={'username': 'username2', 'id': '1'}),
            data={'format': 'json', 'skor': '101'}
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

        response = self.client.put(
            reverse('laporan_praktikum:supervisor-sekolah-nilai-laporan-mingguan-mahasiswa',
            kwargs={'username': 'username2', 'id': '1'}),
            data={'format': 'json', 'skor': 'aa'}
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_can_not_update_skor_supervisor_sekolah_because_of_no_user(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_supervisor_sekolah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.put(
            reverse('laporan_praktikum:supervisor-sekolah-nilai-laporan-mingguan-mahasiswa',
            kwargs={'username': 'usernamefake', 'id': '1'}),
            data={'format': 'json', 'skor': '50'}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_update_skor_supervisor_sekolah_because_of_no_laporan(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_supervisor_sekolah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.put(
            reverse('laporan_praktikum:supervisor-sekolah-nilai-laporan-mingguan-mahasiswa',
            kwargs={'username': 'username2', 'id': '2'}),
            data={'format': 'json', 'skor': '50'}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_not_update_skor_supervisor_sekolah_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=token_type + 'falsetoken')
        response = self.client.put(
            reverse('laporan_praktikum:supervisor-sekolah-nilai-laporan-mingguan-mahasiswa',
            kwargs={'username': 'username2', 'id': '1'}),
            data={'format': 'json', 'skor': '50'}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_update_skor_other_role_in_login_supervisor_sekolah(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_mahasiswa)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION=token_type + token)
        response = self.client.put(
            reverse('laporan_praktikum:supervisor-sekolah-nilai-laporan-mingguan-mahasiswa',
            kwargs={'username': 'username3', 'id': '1'}),
            data={'format': 'json', 'skor': '50'}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
