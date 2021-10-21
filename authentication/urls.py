from . import views
from .cas_wrapper import APILoginView, APILogoutView
from django.urls import include, path

app_name = 'authentication'
urlpatterns = [
    path('login/sivitas/', APILoginView.as_view(), name='login-sivitas'),
    path('logout/', views.ManualLogoutView.as_view(), name='logout'),
    path('register/supervisor-lembaga/', views.UserRegistrationView.as_view(), name='register-supervisor-lembaga'),
    path('login/supervisor-lembaga/', views.UserLoginView.as_view(), name='login-supervisor-lembaga'),
    path('register/supervisor-lembaga/', views.UserRegistrationView.as_view(), name='register-supervisor-lembaga'),
    path('login/administrator/', views.AdministratorLoginView.as_view(), name='login-administrator'),
    path('profile/mahasiswa', views.UserProfileMahasiswaView.as_view(), name='profile-mahasiswa'),
    path('login/supervisor-sekolah/', views.UserLoginView.as_view(), name='login-supervisor-sekolah'),
    path('profile/supervisor-sekolah', views.UserProfileSupervisorSekolahView.as_view(), name='profile-supervisor-sekolah'),
    path('profile/supervisor-lembaga', views.UserProfileSupervisorLembagaView.as_view(), name='profile-supervisor-lembaga'),
    path('login/koordinator-kuliah/', views.UserLoginView.as_view(), name='login-koordinator-kuliah'),
    path('profile/koordinator-kuliah', views.UserProfileKoordinatorKuliahView.as_view(), name='profile-koordinator-kuliah'),
    path('profile/administrator', views.UserProfileAdministratorView.as_view(), name='profile-administrator'),
    path('profile/user', views.UserProfileUserView.as_view(), name='profile-user'),
    path('periode/list', views.PeriodeListView.as_view(), name='periode-list'),
    path('login/sso/', views.ManualSSOLoginView.as_view(), name='login-sso'),
]
