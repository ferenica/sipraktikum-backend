from .models import (
    User,
    Mahasiswa,
    SupervisorLembaga,
    SupervisorSekolah,
    KoordinatorKuliah,
    Administrator,
    Periode
)
from .serializers import (
    MahasiswaSerializer,
    KoordinatorKuliahSerializer,
    SupervisorLembagaSerializer,
    SupervisorSekolahSerializer,
    AdministratorSerializer,
    SupervisorLembagaRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    PeriodeSerializer,
    ManualSSOLoginSerializer,
    AdministratorLoginSerializer
)
from .role import Role
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import update_last_login
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

factory = APIRequestFactory()
request = factory.get('/')

serializer_context = {
    'request': Request(request),
}

response_field = ['success', 'status_code', 'message']
profile_success_message = 'User profile fetched successfully'

STR_CANNOT_FIND_USER_SUPERVISOR_SEKOLAH = 'Can not find user data for Supervisor Sekolah'


class UserRegistrationView(CreateAPIView):  # pragma: no cover

    permission_classes = (AllowAny,)
    serializer_class = SupervisorLembagaRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: 'User registered successfully',
        }

        return Response(response, status=status.HTTP_201_CREATED)


class UserLoginView(RetrieveAPIView):  # pragma: no cover

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: 'User logged in successfully',
            'token': serializer.data['token'],
        }

        return Response(response, status=status.HTTP_200_OK)


class ManualSSOLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ManualSSOLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: 'User logged in successfully',
            'token': serializer.data['token'],
            'role': serializer.data['role']
        }

        return Response(response, status=status.HTTP_200_OK)


class ManualLogoutView(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        update_last_login(datetime.now(), request.user)
        return HttpResponseRedirect("http://ppl-berkah.herokuapp.com/")


class UserProfileMahasiswaView(RetrieveAPIView):  # pragma: no cover

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            profile = Mahasiswa.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            serializer = MahasiswaSerializer(profile, context={'request': request})
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: profile_success_message,
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


class AdministratorLoginView(RetrieveAPIView):  # pragma: no cover

    permission_classes = (AllowAny,)
    serializer_class = AdministratorLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        response = {
            response_field[0]: 'True',
            response_field[1]: status_code,
            response_field[2]: 'User logged in successfully',
            'token': serializer.data['token'],
        }

        return Response(response, status=status.HTTP_200_OK)


class UserProfileSupervisorSekolahView(RetrieveAPIView):  # pragma: no cover

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            profile = SupervisorSekolah.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            serializer = SupervisorSekolahSerializer(profile, context={'request': request})
            response = {
                response_field[0]: 'True',
                response_field[1]: status_code,
                response_field[2]: profile_success_message,
                'data': serializer.data
            }
        except SupervisorSekolah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: STR_CANNOT_FIND_USER_SUPERVISOR_SEKOLAH
            }
        return Response(response, status=status_code)


class UserProfileSupervisorLembagaView(RetrieveAPIView):  # pragma: no cover

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            profile = SupervisorLembaga.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            serializer = SupervisorLembagaSerializer(profile, context={'request': request})
            response = {
                response_field[0]: 'true',
                response_field[1]: status_code,
                response_field[2]: profile_success_message,
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


class UserProfileKoordinatorKuliahView(RetrieveAPIView):  # pragma: no cover

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            profile = KoordinatorKuliah.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            serializer = KoordinatorKuliahSerializer(profile, context={'request': request})
            response = {
                response_field[0]: 'true',
                response_field[1]: status_code,
                response_field[2]: profile_success_message,
                'data': serializer.data
            }
        except KoordinatorKuliah.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Can not find user data for Koordinator Praktikum'
            }
        return Response(response, status=status_code)


class UserProfileAdministratorView(RetrieveAPIView):  # pragma: no cover

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            profile = Administrator.objects.get(user=user)
            status_code = status.HTTP_200_OK
            serializer = AdministratorSerializer(profile, context={'request': request})
            response = {
                response_field[0]: 'true',
                response_field[1]: status_code,
                response_field[2]: profile_success_message,
                'data': serializer.data
            }
        except Administrator.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                response_field[0]: 'False',
                response_field[1]: status_code,
                response_field[2]: 'Can not find user data for Administrator',
            }
        return Response(response, status=status_code)


class UserProfileUserView(RetrieveAPIView):  # pragma: no cover

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        user_data = User.objects.get(email=request.user.email)
        status_code = status.HTTP_200_OK
        serializer = UserSerializer(user_data, context={'request': request})
        response = {
            response_field[0]: 'true',
            response_field[1]: status_code,
            response_field[2]: profile_success_message,
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class PeriodeListView(RetrieveAPIView):
    """
    Provides a get method handler.
    """
    permission_classes = (AllowAny, )
    serializer_class = PeriodeSerializer

    def get(self, request):
        data = Periode.objects.all()
        serializer = PeriodeSerializer(data, context={'request': request}, many=True)

        status_code = status.HTTP_200_OK
        response = {
            response_field[0]: 'true',
            response_field[1]: status_code,
            response_field[2]: "Success fetched data",
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
