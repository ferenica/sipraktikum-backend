from rest_framework import serializers
from django.contrib.auth.models import update_last_login
from .models import (
    User,
    Role,
    Mahasiswa,
    SupervisorLembaga,
    SupervisorSekolah,
    KoordinatorKuliah,
    Administrator,
    Periode,
    Config
)
from .manualSSO import SSOClass
from lembaga.models import Lembaga
from lembaga.serializers import LembagaSerializer
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate

import datetime

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class PeriodeSerializer(serializers.ModelSerializer):
    """Periode serializer json field."""

    class Meta:
        model = Periode
        fields = ['id', 'nama']


class ConfigSerializer(serializers.ModelSerializer):
    """Periode serializer json field."""

    class Meta:
        model = Config
        fields = ['key', 'value']


class UserSerializer(serializers.ModelSerializer):
    """User serializer json field."""

    full_name = serializers.CharField(source='get_full_name')
    role = serializers.CharField(source='role.role')
    lembaga = serializers.CharField(source='supervisor_lembaga.lembaga')

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'role', 'is_active', 'lembaga']


class AdministratorSerializer(serializers.ModelSerializer):
    """Administrator serializer json field."""

    user = UserSerializer()

    class Meta:
        model = Administrator
        fields = ['user', 'nip']


class KoordinatorKuliahSerializer(serializers.ModelSerializer):
    """Koordinator Kuliah serializer json field."""

    user = UserSerializer()

    class Meta:
        model = KoordinatorKuliah
        fields = ['user', 'nip']


class SupervisorSekolahSerializer(serializers.ModelSerializer):
    """Supervisor Sekolah serializer json field."""

    user = UserSerializer()

    class Meta:
        model = SupervisorSekolah
        fields = ['user', 'nip']


class SupervisorLembagaSerializer(serializers.ModelSerializer):
    """Supervisor Lembaga serializer json field."""

    user = UserSerializer()
    lembaga = LembagaSerializer()

    class Meta:
        model = SupervisorLembaga
        fields = ['user', 'lembaga', 'jabatan']


class MahasiswaSerializer(serializers.ModelSerializer):
    """Mahasiswa serializer json field."""

    user = UserSerializer()
    supervisor_sekolah = SupervisorSekolahSerializer()
    supervisor_lembaga = SupervisorLembagaSerializer()
    periode = PeriodeSerializer()

    class Meta:
        model = Mahasiswa
        fields = [
            'user',
            'org_code',
            'npm',
            'periode',
            'faculty',
            'major',
            'program',
            'supervisor_sekolah',
            'supervisor_lembaga'
        ]


class LembagaProfileSerializer(serializers.ModelSerializer):
    """Lembaga Profile serializer json field."""

    class Meta:
        model = SupervisorLembaga
        fields = ['lembaga', 'jabatan']


class SupervisorLembagaRegistrationSerializer(serializers.ModelSerializer):
    """Serializer json field for registration."""

    profile = LembagaProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):  # pragma: no cover
        profile_data = validated_data.pop('profile')
        try:
            lembaga = Lembaga.objects.get(nama=profile_data['lembaga'])
            user = User.objects.create_user(**validated_data)
            user.is_active = False
            user.save()
            SupervisorLembaga.objects.create(
                user=user,
                lembaga=lembaga,
                jabatan=profile_data['jabatan']
            )
            Role.objects.create(
                user=user,
                role='Supervisor Lembaga'
            )
            return user
        except Lembaga.DoesNotExist:
            raise serializers.ValidationError(
                'Lembaga tidak ditemukan'
            )


class UserLoginSerializer(serializers.Serializer):
    """Serializer json field for login."""

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        try:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError(
                    'User with given email and password does not exists'
                )
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
            username = user.username
            return {
                'username': user.username,
                'token': jwt_token
            }
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )


class AdministratorLoginSerializer(serializers.Serializer):
    """Serializer json field for login."""

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        try:
            user = authenticate(username=username, password=password)
            Administrator.objects.get(user=User.objects.get(username=username).id)
            if user is None:
                raise serializers.ValidationError(
                    'User with given email and password does not exists'
                )
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
            username = user.username
            return {
                'username': user.username,
                'token': jwt_token
            }
        except Administrator.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )


class ManualSSOLoginSerializer(serializers.Serializer):
    """Serializer json field for login."""

    role = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        role = data.get("role", None)
        ssoLogin = SSOClass(username, password)
        ssoLogin.login()
        if ssoLogin.checkLogin():
            user = User.objects.get(username=username)
            if user is None:
                raise serializers.ValidationError(
                    'User with the given username / password does not exists'
                )
            try:
                if role == "Supervisor Sekolah":
                    if SupervisorSekolah.objects.get(user=user):
                        role = "Supervisor"
                elif role == "Mahasiswa":
                    if Mahasiswa.objects.get(user=user):
                        role = "Mahasiswa"
                elif role == "Koordinator Praktikum":
                    if KoordinatorKuliah.objects.get(user=user):
                        role = "Koordinator Praktikum"
                else:
                    raise serializers.ValidationError('Invalid role')
            except Mahasiswa.DoesNotExist:
                raise serializers.ValidationError('You are not Mahasiswa')
            except SupervisorSekolah.DoesNotExist:
                raise serializers.ValidationError('You are not Supervisor Sekolah')
            except KoordinatorKuliah.DoesNotExist:
                raise serializers.ValidationError('You are not Koordinator Praktikum')
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
            username = user.username
            return {
                'username': user.username,
                'token': jwt_token,
                'role': role
            }
        else:
            raise serializers.ValidationError('Username / Password SSO is not valid')
