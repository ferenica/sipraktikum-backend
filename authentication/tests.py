from .models import (
    ORG_CODE,
    User,
    Mahasiswa,
    SupervisorLembaga,
    SupervisorSekolah,
    KoordinatorKuliah,
    Administrator,
    Periode
)
from lembaga.models import (
    Institusi,
    Tema,
    Lembaga,
)
from .serializers import (
    UserSerializer,
    LembagaProfileSerializer,
    SupervisorLembagaRegistrationSerializer,
    UserLoginSerializer,
    MahasiswaSerializer,
    SupervisorLembagaSerializer,
    SupervisorSekolahSerializer,
    KoordinatorKuliahSerializer,
    AdministratorSerializer,
)
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django_cas_ng.signals import cas_user_authenticated
from rest_framework import serializers
from rest_framework import status
from rest_framework.test import APITestCase
import json
from .role import Role
from rest_framework_jwt.settings import api_settings
from django.core.files import File
from io import BytesIO
from PIL import Image
import base64


class ModelsTest(TestCase):
    '''Test Module for model'''

    def get_image_file(self, name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        '''Mock image'''
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        ''' Create object to test based on models'''

        user_mahasiswa = User.objects.create_user(
            username="username1",
            email="username1@email.com",
            password="password",
            first_name="User",
            last_name="Name1"
        )

        user_supervisor_sekolah = User.objects.create_user(
            username="username2",
            email="username2@email.com",
            password="password",
            first_name="User",
            last_name="Name2"
        )

        user_supervisor_lembaga = User.objects.create_user(
            username="username3",
            email="username3@email.com",
            password="password",
            first_name="User",
            last_name="Name3"
        )

        user_koordinator_kuliah = User.objects.create_user(
            username="username4",
            email="username4@email.com",
            password="password",
            first_name="User",
            last_name="Name4"
        )

        user_administrator = User.objects.create_user(
            username="username5",
            email="username5@email.com",
            password="password",
            first_name="User",
            last_name="Name5"
        )

        User.objects.create_superuser(
            username="admin",
            email="username6@email.com",
            password="password"
        )

        institusi = Institusi.objects.create(
            nama="testing"
        )

        tema = Tema.objects.create(
            nama="testing"
        )
        self.lembaga = Lembaga.objects.create(
            nama="testing",
            jenis_pelayanan="testing",
            institusi=institusi,
            tema=tema,
            deskripsi_singkat="testing",
            praktikum_ke=1,
            alamat="test_alamat",
            beneficaries="test_beneficaries"
        )

        self.lembaga.gambar = self.get_image_file()
        self.lembaga.save()

        supervisor_lembaga = SupervisorLembaga.objects.create(
            user=user_supervisor_lembaga,
            lembaga=self.lembaga,
            jabatan="jabatan"
        )

        supervisor_sekolah = SupervisorSekolah.objects.create(
            user=user_supervisor_sekolah,
            nip="nip"
        )

        periode = Periode.objects.create(
            nama="periode"
        )

        Mahasiswa.objects.create(
            user=user_mahasiswa,
            npm="npm",
            org_code="org_code",
            faculty="faculty",
            major="major",
            program="program",
            periode=periode,
            supervisor_lembaga=supervisor_lembaga,
            supervisor_sekolah=supervisor_sekolah
        )

        KoordinatorKuliah.objects.create(
            user=user_koordinator_kuliah,
            nip="nip"
        )

        Administrator.objects.create(
            user=user_administrator,
            nip="nip"
        )

    def test_model_user_return_str(self):
        ''' Test model user return true if the result is string type'''

        user_mahasiswa_data = User.objects.get(username="username1")
        self.assertEqual(user_mahasiswa_data.username, "username1")
        self.assertEqual(user_mahasiswa_data.email, "username1@email.com")
        self.assertEqual(user_mahasiswa_data.get_full_name(), "User Name1")
        self.assertEqual(type(user_mahasiswa_data.__str__()), str)

        user_supervisor_sekolah_data = User.objects.get(username="username2")
        self.assertEqual(user_supervisor_sekolah_data.username, "username2")
        self.assertEqual(user_supervisor_sekolah_data.email, "username2@email.com")
        self.assertEqual(user_supervisor_sekolah_data.get_full_name(), "User Name2")
        self.assertEqual(type(user_supervisor_sekolah_data.__str__()), str)

        user_supervisor_lembaga_data = User.objects.get(username="username3")
        self.assertEqual(user_supervisor_lembaga_data.username, "username3")
        self.assertEqual(user_supervisor_lembaga_data.email, "username3@email.com")
        self.assertEqual(user_supervisor_lembaga_data.get_full_name(), "User Name3")
        self.assertEqual(type(user_supervisor_lembaga_data.__str__()), str)

        user_koordinator_kuliah_data = User.objects.get(username="username4")
        self.assertEqual(user_koordinator_kuliah_data.username, "username4")
        self.assertEqual(user_koordinator_kuliah_data.email, "username4@email.com")
        self.assertEqual(user_koordinator_kuliah_data.get_full_name(), "User Name4")
        self.assertEqual(type(user_koordinator_kuliah_data.__str__()), str)

        user_administrator_data = User.objects.get(username="username5")
        self.assertEqual(user_administrator_data.username, "username5")
        self.assertEqual(user_administrator_data.email, "username5@email.com")
        self.assertEqual(user_administrator_data.get_full_name(), "User Name5")
        self.assertEqual(type(user_administrator_data.__str__()), str)

        super_user_data = User.objects.get(username="admin")
        self.assertEqual(super_user_data.username, "admin")
        self.assertEqual(super_user_data.email, "username6@email.com")
        self.assertEqual(super_user_data.get_full_name(), "")
        self.assertEqual(type(super_user_data.__str__()), str)

    def test_model_profile_return_str(self):
        ''' Test model profile return true if the result is string type'''

        user_mahasiswa_data = User.objects.get(username="username1")
        user_supervisor_sekolah_data = User.objects.get(username="username2")
        user_supervisor_lembaga_data = User.objects.get(username="username3")
        user_koordinator_kuliah_data = User.objects.get(username="username4")
        user_administrator_data = User.objects.get(username="username5")

        profile_mahasiswa_data = Mahasiswa.objects.get(user=user_mahasiswa_data)
        self.assertEqual(profile_mahasiswa_data.org_code, "org_code")
        self.assertEqual(profile_mahasiswa_data.npm, "npm")
        self.assertEqual(profile_mahasiswa_data.faculty, "faculty")
        self.assertEqual(profile_mahasiswa_data.major, "major")
        self.assertEqual(profile_mahasiswa_data.program, "program")
        self.assertEqual(profile_mahasiswa_data.supervisor_lembaga.user, user_supervisor_lembaga_data)
        self.assertEqual(profile_mahasiswa_data.supervisor_sekolah.user, user_supervisor_sekolah_data)
        self.assertEqual(type(profile_mahasiswa_data.__str__()), str)

        profile_supervisor_lembaga_data = SupervisorLembaga.objects.get(user=user_supervisor_lembaga_data)
        self.assertEqual(profile_supervisor_lembaga_data.lembaga, self.lembaga)
        self.assertEqual(profile_supervisor_lembaga_data.jabatan, "jabatan")
        self.assertEqual(type(profile_supervisor_lembaga_data.__str__()), str)

        profile_supervisor_sekolah_data = SupervisorSekolah.objects.get(user=user_supervisor_sekolah_data)
        self.assertEqual(profile_supervisor_sekolah_data.nip, "nip")
        self.assertEqual(type(profile_supervisor_sekolah_data.__str__()), str)

        profile_koordinator_kuliah_data = KoordinatorKuliah.objects.get(user=user_koordinator_kuliah_data)
        self.assertEqual(profile_koordinator_kuliah_data.nip, "nip")
        self.assertEqual(type(profile_koordinator_kuliah_data.__str__()), str)

        profile_administrator_data = Administrator.objects.get(user=user_administrator_data)
        self.assertEqual(profile_administrator_data.nip, "nip")
        self.assertEqual(type(profile_administrator_data.__str__()), str)


class SerializersTest(TestCase):

    def get_image_file(self, name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        '''Mock image'''
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        user_mahasiswa = User.objects.create_user(
            username="username1",
            email="username1@email.com",
            password="password",
            first_name="User",
            last_name="Name1"
        )

        user_supervisor_sekolah = User.objects.create_user(
            username="username2",
            email="username2@email.com",
            password="password",
            first_name="User",
            last_name="Name2"
        )

        user_supervisor_lembaga = User.objects.create_user(
            username="username3",
            email="username3@email.com",
            password="password",
            first_name="User",
            last_name="Name3"
        )

        user_koordinator_kuliah = User.objects.create_user(
            username="username4",
            email="username4@email.com",
            password="password",
            first_name="User",
            last_name="Name4"
        )

        user_administrator = User.objects.create_user(
            username="username5",
            email="username5@email.com",
            password="password",
            first_name="User",
            last_name="Name5"
        )

        institusi = Institusi.objects.create(
            nama="testing"
        )

        tema = Tema.objects.create(
            nama="testing"
        )

        self.lembaga = Lembaga.objects.create(
            nama="testing",
            jenis_pelayanan="testing",
            institusi=institusi,
            tema=tema,
            deskripsi_singkat="testing",
            praktikum_ke=1,
            beneficaries="test_beneficaries",
            alamat="test_alamat"
        )

        self.lembaga.gambar = self.get_image_file()
        self.lembaga.save()

        profile_supervisor_lembaga = SupervisorLembaga.objects.create(
            user=user_supervisor_lembaga,
            lembaga=self.lembaga,
            jabatan="jabatan"
        )

        profile_supervisor_sekolah = SupervisorSekolah.objects.create(
            user=user_supervisor_sekolah,
            nip="nip"
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
            supervisor_lembaga=profile_supervisor_lembaga,
            supervisor_sekolah=profile_supervisor_sekolah
        )

        profile_koordinator_kuliah = KoordinatorKuliah.objects.create(
            user=user_koordinator_kuliah,
            nip="nip"
        )

        profile_administrator = Administrator.objects.create(
            user=user_administrator,
            nip="nip"
        )

        self.user_serializer = UserSerializer(user_mahasiswa)
        self.mahasiswa_serializer = MahasiswaSerializer(profile_mahasiswa)
        self.supervisor_lembaga_serializer = SupervisorLembagaSerializer(profile_supervisor_lembaga)
        self.supervisor_sekolah_serializer = SupervisorSekolahSerializer(profile_supervisor_sekolah)
        self.koordinator_kuliah_serializer = KoordinatorKuliahSerializer(profile_koordinator_kuliah)
        self.administrator_serializer = AdministratorSerializer(profile_administrator)
        self.lembaga_profile_serializer = LembagaProfileSerializer(profile_supervisor_lembaga)
        self.user_registration_serializer = SupervisorLembagaRegistrationSerializer(user_supervisor_lembaga)
        self.user_login_serializer = UserLoginSerializer(user_supervisor_lembaga)

        self.registration_data = {
            "username": "dhafin",
            "full_name": "Razaqa Dhafin",
            "email": "dhafin@test.com",
            "password": "1234567",
            "profile": {
                "lembaga": self.lembaga.id,
                "jabatan": "Test Jabatan"
            }
        }

        self.registration_data_invalid_lembaga = {
            "username": "dhafin",
            "full_name": "Razaqa Dhafin",
            "email": "dhafin@test.com",
            "password": "1234567",
            "profile": {
                "lembaga": "fake",
                "jabatan": "Test Jabatan"
            }
        }

        self.login_data_invalid = {
            "username": "dhafin",
            "password": "1234567"
        }

        self.login_data_valid = {
            "username": "username2",
            "password": "password"
        }

    def test_user_serializer_contains_valid_data(self):
        data = self.user_serializer.data
        self.assertEqual(
            set(data),
            set(['username', 'email', 'full_name', 'role', 'is_active', 'lembaga'])
        )

    def test_profile_mahasiswa_serializer_contains_valid_data(self):
        data = self.mahasiswa_serializer.data
        self.assertEqual(
            set(data),
            set([
                'user',
                'org_code',
                'npm',
                'faculty',
                'major',
                'program',
                'periode',
                'supervisor_lembaga',
                'supervisor_sekolah'
            ])
        )

    def test_profile_supervisor_sekolah_serializer_contains_valid_data(self):
        data = self.supervisor_sekolah_serializer.data
        self.assertEqual(
            set(data),
            set(['user', 'nip'])
        )

    def test_profile_koordinator_kuliah_serializer_contains_valid_data(self):
        data = self.koordinator_kuliah_serializer.data
        self.assertEqual(
            set(data),
            set(['user', 'nip'])
        )

    def test_profile_supervisor_lembaga_serializer_contains_valid_data(self):
        data = self.supervisor_lembaga_serializer.data
        self.assertEqual(
            set(data),
            set(['user', 'lembaga', 'jabatan'])
        )

    def test_profile_administrator_serializer_contains_valid_data(self):
        data = self.administrator_serializer.data
        self.assertEqual(
            set(data),
            set(['user', 'nip'])
        )

    def test_lembaga_profile_serializer_contains_valid_data(self):
        data = self.lembaga_profile_serializer.data
        self.assertEqual(
            set(data),
            set(['lembaga', 'jabatan'])
        )

    def test_user_registration_serializer_contains_valid_data(self):
        data = self.user_registration_serializer.data
        self.assertEqual(
            set(data),
            set(['username', 'first_name', 'last_name', 'email'])
        )

    def test_user_login_serializer_contains_valid_data(self):
        data = self.user_login_serializer.data
        self.assertEqual(
            set(data),
            set(['username'])
        )

    def test_user_login_serializer_validate_with_valid_data_return_user_data(self):
        data = self.user_login_serializer
        self.assertEqual(
            data.validate(self.login_data_valid).get("username"),
            "username2"
        )

    def test_user_login_serializer_validate_with_invalid_data(self):
        data = self.user_login_serializer
        with self.assertRaises(serializers.ValidationError):
            data.validate(self.login_data_invalid).get("username")

    def test_user_register_serializer_validate_with_invalid_lembaga(self):
        data = self.user_registration_serializer
        with self.assertRaises(serializers.ValidationError):
            data.create(self.registration_data_invalid_lembaga)


class SSOUITest(TestCase):
    """Test SSO UI app."""

    ATTRIBUTES_MAHASISWA = {
        "nama": "Ice Bear",
        "peran_user": "mahasiswa",
        "npm": "1706123123",
        "kd_org": "01.00.12.01"
    }

    ATTRIBUTES_STAFF = {
        "nama": "Ice Bear",
        "peran_user": "staff",
        "nip": "1706123123"
    }

    ATTRIBUTES_OTHER = {
        "nama": "Ice Bear",
        "peran_user": "pegawai",
        "nip": "1706123123"
    }

    def setUp(self):
        """Set up test."""
        self.user_mahasiswa = User.objects.create_user(
            username='username1',
            password='password',
            email='username1@ui.ac.id',
            first_name="Ice",
            last_name="Bear"
        )
        self.user_staff = User.objects.create_user(
            username='username2',
            password='password',
            email='username2@ui.ac.id',
            first_name="Ice",
            last_name="Bear"
        )
        self.user_other = User.objects.create_user(
            username='username3',
            password='password',
            email='username3@ui.ac.id',
            first_name="Ice",
            last_name="Bear"
        )

        SupervisorSekolah.objects.create(
            user=self.user_staff,
            nip="1706123123"
        )

        Administrator.objects.create(
            user=self.user_other,
            nip="1706123123"
        )

        Mahasiswa.objects.create(
            user=self.user_mahasiswa,
            npm="1706123123",
            org_code="01.00.12.01",
            faculty="faculty",
            major="major",
            program="program",
            periode=None,
            supervisor_lembaga=None,
            supervisor_sekolah=None
        )

    def test_profile_can_save_attributes_if_user_staff_not_yet_registered(self):
        """Test if Profile Staff model can save the attributes from CAS."""
        cas_user_authenticated.send(
            sender=self,
            user=self.user_staff,
            username=self.user_staff.username,
            created=False,
            attributes=SSOUITest.ATTRIBUTES_STAFF
        )
        self.profile = SupervisorSekolah.objects.get(user=self.user_staff)
        self.assertJSONEqual(
            json.dumps({
                "nama": self.user_staff.get_full_name(),
                "peran_user": "staff",
                "nip": self.profile.nip
            }),
            SSOUITest.ATTRIBUTES_STAFF
        )
        self.assertEqual(self.user_staff.email, f"{self.user_staff.username}@ui.ac.id")
        self.assertEqual(self.user_staff.get_full_name(), "Ice Bear")

    def test_profile_can_save_attributes_if_user_other_not_yet_registered(self):
        """Test if Profile Other model can save the attributes from CAS."""
        cas_user_authenticated.send(
            sender=self,
            user=self.user_other,
            username=self.user_other.username,
            created=False,
            attributes=SSOUITest.ATTRIBUTES_OTHER
        )
        self.profile = Administrator.objects.get(user=self.user_other)
        self.assertJSONEqual(
            json.dumps({
                "nama": self.user_other.get_full_name(),
                "peran_user": "pegawai",
                "nip": self.profile.nip
            }),
            SSOUITest.ATTRIBUTES_OTHER
        )
        self.assertEqual(self.user_other.email, f"{self.user_other.username}@ui.ac.id")
        self.assertEqual(self.user_other.get_full_name(), "Ice Bear")


class AuthenticationJSONWebTokenTest(APITestCase):

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
        '''
        self.registration_data = {
            "username": "user1",
            "full_name": "User Name1",
            "email": "user1@test.com",
            "password": "1234567",
            "profile": {
                "lembaga": 0,
                "jabatan": "jabatan1"
            }
        }

        self.registration_data_unknown_lembaga = {
            "username": "dhafin",
            "full_name": "Razaqa Dhafin",
            "email": "dhafin@test.com",
            "password": "1234567",
            "profile": {
                "lembaga": "fake",
                "jabatan": "Test Jabatan"
            }
        }
        '''
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

        self.user_koordinator_kuliah = User.objects.create_user(
            username="username5",
            email="username5@email.com",
            password="password",
            first_name="User",
            last_name="Name5"
        )

        self.user_administrator = User.objects.create_user(
            username="username6",
            email="username6@email.com",
            password="password",
            first_name="User",
            last_name="Name6"
        )

        institusi = Institusi.objects.create(
            nama="testing"
        )

        tema = Tema.objects.create(
            nama="testing"
        )

        self.lembaga = Lembaga.objects.create(
            nama="testing",
            jenis_pelayanan="testing",
            institusi=institusi,
            tema=tema,
            deskripsi_singkat="testing",
            praktikum_ke=1,
            beneficaries="test_beneficaries",
            alamat="test_alamat"
        )

        self.lembaga.gambar = self.get_image_file()
        self.lembaga.save()

        supervisor_lembaga = SupervisorLembaga.objects.create(
            user=self.user_supervisor_lembaga,
            lembaga=self.lembaga,
            jabatan="jabatan"
        )

        supervisor_sekolah = SupervisorSekolah.objects.create(
            user=self.user_supervisor_sekolah,
            nip="nip"
        )

        KoordinatorKuliah.objects.create(
            user=self.user_koordinator_kuliah,
            nip="nip"
        )

        Administrator.objects.create(
            user=self.user_administrator,
            nip="nip"
        )

        periode = Periode.objects.create(
            nama="periode"
        )

        Mahasiswa.objects.create(
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

        self.registration_data = {
            "username": "usernamevalid1",
            "first_name": "User",
            "last_name": "Name1",
            "email": "usernamevalid1@test.com",
            "password": "123456789",
            "profile": {
                "lembaga": "testing",
                "jabatan": "jabatan1"
            }
        }

        self.registration_data_unknown_lembaga = {
            "username": "dhafin",
            "first_name": "Razaqa Dhafin",
            "last_name": "Razaqa Dhafin",
            "email": "dhafin@test.com",
            "password": "1234567",
            "profile": {
                "lembaga": "fake",
                "jabatan": "Test Jabatan"
            }
        }

        self.login_data_mahasiswa_valid = {
            "username": "username2",
            "password": "password"
        }

        self.login_data_supervisor_sekolah_valid = {
            "username": "username3",
            "password": "password"
        }

        self.login_data_supervisor_lembaga_valid = {
            "username": "username4",
            "password": "password"
        }

        self.login_data_supervisor_lembaga_invalid_wrong_password = {
            "username": "username4",
            "password": "wrong"
        }

        self.login_data_koordinator_kuliah_valid = {
            "username": "username5",
            "password": "password"
        }

        self.login_data_administrator_valid = {
            "username": "username6",
            "password": "password"
        }

        self.login_data_invalid = {
            "username": "username10",
            "password": "password"
        }

    def test_can_not_register_user_if_lembaga_does_not_exist(self):
        response = self.client.post(reverse('authentication:register-supervisor-lembaga'), self.registration_data_unknown_lembaga)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_not_register_same_user_twice(self):
        self.client.post(reverse('authentication:register-supervisor-lembaga'), self.registration_data)
        response = self.client.post(reverse('authentication:register-supervisor-lembaga'), self.registration_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Mahasiswa

    def test_can_see_profile_mahasiswa_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_mahasiswa)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('authentication:profile-mahasiswa'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_profile_mahasiswa_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'falsetoken')
        response = self.client.get(reverse('authentication:profile-mahasiswa'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_profile_other_role_in_login_mahasiswa(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('authentication:profile-mahasiswa'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_manual_sso_login_for_mahasiswa_without_role(self):
        response = self.client.post(reverse('authentication:login-sso'), {"username": "test", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_manual_sso_login_for_mahasiswa_with_invalid_role(self):
        response = self.client.post(reverse('authentication:login-sso'), {"username": "test", "password": "test", "role": "Supervisor Sekolah"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_manual_sso_login_for_mahasiswa_with_valid_role(self):
        response = self.client.post(reverse('authentication:login-sso'), {"username": "test", "password": "test", "role": "Mahasiswa"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Supervisor Sekolah

    def test_supervisor_sekolah_can_login_in_web_login_not_sso(self):
        response = self.client.post(reverse('authentication:login-supervisor-sekolah'), self.login_data_supervisor_lembaga_valid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_see_profile_supervisor_sekolah_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_supervisor_sekolah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('authentication:profile-supervisor-sekolah'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_profile_supervisor_sekolah_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'falsetoken')
        response = self.client.get(reverse('authentication:profile-supervisor-sekolah'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_profile_other_role_in_login_supervisor_sekolah(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_mahasiswa)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('authentication:profile-supervisor-sekolah'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_manual_sso_login_for_supervisor_sekolah_without_role(self):
        response = self.client.post(reverse('authentication:login-sso'), {"username": "test", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_manual_sso_login_for_supervisor_sekolah_with_valid_role(self):
        response = self.client.post(reverse('authentication:login-sso'), {"username": "test", "password": "test", "role": "Supervisor Sekolah"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_manual_sso_login_for_supervisor_sekolah_with_invalid_role(self):
        response = self.client.post(reverse('authentication:login-sso'), {"username": "test", "password": "test", "role": "Mahasiswa"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Supervisor Lembaga

    def test_can_login_user_supervisor_lembaga_after_register(self):
        response = self.client.post(reverse('authentication:login-supervisor-lembaga'), self.login_data_supervisor_lembaga_valid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data['token']), str)

    def test_can_not_login_user_supervisor_lembaga_after_register_if_wrong_password(self):
        response = self.client.post(reverse('authentication:login-supervisor-lembaga'), self.login_data_supervisor_lembaga_invalid_wrong_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_not_login_user_supervisor_lembaga_before_register(self):
        response = self.client.post(reverse('authentication:login-supervisor-lembaga'), self.login_data_invalid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_see_profile_supervisor_lembaga_after_login(self):
        response_login = self.client.post(reverse('authentication:login-supervisor-lembaga'), self.login_data_supervisor_lembaga_valid)
        token = response_login.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('authentication:profile-supervisor-lembaga'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_profile_supervisor_lembaga_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'falsetoken')
        response = self.client.get(reverse('authentication:profile-supervisor-lembaga'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_profile_other_role_in_login_supervisor_lembaga(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_supervisor_sekolah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('authentication:profile-supervisor-lembaga'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_login_user_supervisor_lembaga_in_administrator_auth_api(self):
        response = self.client.post(reverse('authentication:login-administrator'), self.login_data_supervisor_lembaga_valid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Koordinator Kuliah

    def test_koordinator_kuliah_can_login_in_web_login_not_sso(self):
        response = self.client.post(reverse('authentication:login-koordinator-kuliah'), self.login_data_koordinator_kuliah_valid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_see_profile_koordinator_kuliah_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('authentication:profile-koordinator-kuliah'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_profile_koordinator_kuliah_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'falsetoken')
        response = self.client.get(reverse('authentication:profile-koordinator-kuliah'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_profile_other_role_in_login_koordinator_kuliah(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_supervisor_lembaga)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('authentication:profile-koordinator-kuliah'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_manual_sso_login_for_koordinator_kuliah_without_role(self):
        response = self.client.post(reverse('authentication:login-sso'), {"username": "test", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_manual_sso_login_for_koordinator_kuliah_with_invalid_role(self):
        response = self.client.post(reverse('authentication:login-sso'), {"username": "test", "password": "test", "role": "Supervisor Sekolah"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_manual_sso_login_for_koordinator_kuliah_with_valid_role(self):
        response = self.client.post(reverse('authentication:login-sso'), {"username": "test", "password": "test", "role": "Koordinator Praktikum"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Administrator

    def test_can_see_profile_administrator_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('authentication:profile-administrator'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_profile_administrator_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'falsetoken')
        response = self.client.get(reverse('authentication:profile-administrator'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_not_see_profile_other_role_in_login_administrator(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_koordinator_kuliah)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('authentication:profile-administrator'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_login_user_administrator_in_administrator_auth_api(self):
        response = self.client.post(reverse('authentication:login-administrator'), self.login_data_administrator_valid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # User

    def test_can_see_profile_user_after_login(self):
        payload = self.JWT_PAYLOAD_HANDLER(self.user_administrator)
        jwt_token = self.JWT_ENCODE_HANDLER(payload)
        token = jwt_token

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('authentication:profile-user'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_see_profile_user_before_login(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'falsetoken')
        response = self.client.get(reverse('authentication:profile-user'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
