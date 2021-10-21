''' Module routing in lembaga app'''
from django.urls import path
from laporan_praktikum import views, views_riwayat
from laporan_praktikum.supervisor_lembaga import views_supv_lembaga
from laporan_praktikum.supervisor_sekolah import views as v_supv_sekolah

# Temp for sprint review
from .views import MahasiswaPraktikumView
from rest_framework import routers
from django.urls import include

# Endpoint Variables
laporan_praktikum_admin = "admin/laporan_praktikum"

app_name = 'laporan_praktikum'

urlpatterns = [

    # Show riwayat praktikum by lembaga
    path('lembaga/praktikum',
        views_riwayat.get_riwayat_laporan_by_lembaga,
        name='list-praktikum-mahasiswa'),
    # Show jenis praktikum mahasiswa
    path('mahasiswa/praktikum/',
        views.UserMahasiswaListPraktikumView.as_view(),
        name='list-praktikum-mahasiswa'),

    # Show laporan mahasiswa list detail
    path('mahasiswa/praktikum/laporan-detail/',
        views.get_list_laporan_praktikum_detail,
        name='laporan-praktikum-mahasiswa'),

    # Get Laporan Mahasiswa By id
    path('mahasiswa/praktikum/laporan-detail/<int:id>/',
        views.get_laporan_mahasiswa_by_id,
        name='laporan-mahasiswa-by-id'),

    # Get Laporan Akhir Mahasiswa By id
    path('mahasiswa/praktikum/laporan-akhir-detail/<int:id>/',
        views.get_laporan_akhir_mahasiswa_by_id,
        name='laporan-akhir-mahasiswa-by-id'),

    # Get Laporan Borang Mahasiswa By id
    path('mahasiswa/praktikum/laporan-borang-detail/<int:id>/',
        views.get_laporan_borang_mahasiswa_by_id,
        name='laporan-borang-mahasiswa-by-id'),

    # Submit link drive laporan mingguan mahasiswa
    path('mahasiswa/praktikum/laporan-detail/submit-link/',
        views.submit_link_laporan_praktikum,
        name='submit-link-laporan-praktikum'),

    # Submit laporan akhir mahasiswa
    path('mahasiswa/praktikum/laporan-akhir/submit/',
        views.crud_submisi_laporan_akhir_mahasiswa,
        name='submit-laporan-akhir-praktikum'),

    # Submit laporan borang mahasiswa
    path('mahasiswa/praktikum/laporan-borang/submit/',
        views.crud_submisi_laporan_borang_mahasiswa,
        name='submit-laporan-akhir-praktikum'),

    # Update laporan praktikum slot mahasiswa
    path('mahasiswa/praktikum/laporan-update/<str:username>/',
        views.get_or_update_laporan_praktikum,
        name='get-or-update-laporan-praktikum'),

    # Delete laporan praktikum slot mahasiswa
    path('mahasiswa/praktikum/laporan-update/<str:username>/delete-laporan/<str:tipe>/<int:pk>/',
        views.delete_laporan_praktikum,
        name='delete-laporan-praktikum'),

    # List Riwayat Laporan Praktikum by mahasiswa
    path('mahasiswa/praktikum/riwayat-laporan/',
        views_riwayat.get_riwayat_laporan_by_mahasiswa,
        name='riwayat-laporan-mahasiswa'),

    # Supervisor Lembaga
    path('supervisor-lembaga/<int:id_lembaga>/',
        views.get_supervisor_lembaga_by_id_lembaga,
        name='list-supervisor-lembaga-by-id-lembaga'),

    path('supervisor-lembaga/user/<str:username>/',
        views.get_supervisor_lembaga_by_username,
        name='list-supervisor-lembaga-by-id-lembaga'),

    path('supervisor-lembaga/praktikum-mahasiswa/riwayat-laporan/',
        views_riwayat.get_riwayat_laporan_by_supervisor_lembaga,
        name='riwayat-laporan-mahasiswa-by-supervisor-lembaga'),

    path('supervisor-lembaga/list-mahasiswa/praktikum/',
        views.UserSupervisorLembagaListMahasiswaView.as_view(),
        name='supervisor-lembaga-list-mahasiswa'),

    path('supervisor-lembaga/list-mahasiswa/praktikum/laporan-akhir/<str:username>/',
        views_supv_lembaga.UserSupervisorLembagaDetailLaporanAkhirMahasiswaView.as_view(),
        name='supervisor-lembaga-detail-laporan-akhir-mahasiswa'),

    path('supervisor-lembaga/praktikum-mahasiswa/nilai/<str:username>/<str:id>/',
    views_supv_lembaga.UserSupervisorLembagaNilaiPraktikumMahasiswaView.as_view(),\
        name='supervisor-sekolah-nilai-praktikum-mahasiswa'),

    # Koordinator Kuliah
    path('koordinator-kuliah/list-mahasiswa/praktikum/',
        views.UserKoordinatorKuliahListMahasiswaView.as_view(),
        name='koordinator-kuliah-list-mahasiswa'),

    # Koordinator Kuliah Grafik Ketepatan Pengumpulan
    path('koordinator-kuliah/riwayat-ketepatan-pengumpulan-laporan',
        views_riwayat.get_riwayat_ketepatan_pengumpulan,
        name='koordinator-kuliah-grafik-pengumpulan-tepat-waktu'),

    # Koordinator Kuliah Chart Persentase Ketepatan Pengumpulan
    path('koordinator-kuliah/persentase-pengumpulan-laporan',
        views_riwayat.get_persentase_ketepatan_pengumpulan,
        name='koordinator-kuliah-persentase-pengumpulan-laporan'),

    # Koordinator Kuliah Chart Persentase Ketepatan Pengumpulan
    path('koordinator-kuliah/persentase-penilaian-laporan-supervisor-sekolah',
        views_riwayat.get_persentase_penilaian_laporan_supervisor_sekolah,
        name='koordinator-kuliah-persentase-penilaian-laporan'),

    # Administrator
    path('administrator/list-user/',
        views.UserAdministratorListUserView.as_view(),
        name='administrator-list-user'),

    # Supervisor Sekolah list praktikum mahasiswa
    path('supervisor-sekolah/list-mahasiswa/praktikum/',
        views.UserSupervisorSekolahListMahasiswaView.as_view(),
        name='supervisor-sekolah-list-mahasiswa'),

    # List Praktikum Mahasiswa by Supervisor Sekolah
    path('supervisor-sekolah/praktikum-mahasiswa/list/<str:username>/',
        views.UserSupervisorSekolahListPraktikumMahasiswaView.as_view(),
        name='supervisor-sekolah-list-praktikum-mahasiswa'),

    # List Riwayat Laporan Praktikum by supervisor Sekolah
    path('supervisor-sekolah/praktikum-mahasiswa/riwayat-laporan/',
        views_riwayat.get_riwayat_laporan_by_supervisor_sekolah,
        name='riwayat-laporan-supervisor-sekolah'),

    # Detail Laporan Mingguan Mahasiswa Supervisor Sekolah by Username Mahasiswa and Id Laporan
    path('supervisor-sekolah/laporan-mingguan-mahasiswa/detail/<str:username>/<str:id>/',
        views.UserSupervisorSekolahDetailLaporanMingguanMahasiswaView.as_view(),
        name='supervisor-sekolah-detail-laporan-mingguan-mahasiswa'),

    # Detail Laporan Akhir Mahasiswa Supervisor Sekolah by Username Mahasiswa and Id Laporan
    path('supervisor-sekolah/laporan-akhir-mahasiswa/detail/<str:username>/<str:id>/',
        views.UserSupervisorSekolahDetailLaporanAkhirMahasiswaView.as_view(),
        name='supervisor-sekolah-detail-laporan-akhir-mahasiswa'),

    # Detail Borang Mahasiswa Supervisor Sekolah by Username Mahasiswa and Id Laporan
    path('supervisor-sekolah/borang-mahasiswa/detail/<str:username>/<str:id>/',
        views.UserSupervisorSekolahDetailBorangMahasiswaView.as_view(),
        name='supervisor-sekolah-detail-borang-mahasiswa'),

    # Update Nilai Laporan Mingguan Mahasiswa Supervisor Sekolah by Username Mahasiswa and Id Laporan
    path('supervisor-sekolah/laporan-mingguan-mahasiswa/nilai/<str:username>/<str:id>/',
        views.UserSupervisorSekolahNilaiLaporanMingguanMahasiswaView.as_view(),
        name='supervisor-sekolah-nilai-laporan-mingguan-mahasiswa'),

    # Update Nilai Laporan Akhir Mahasiswa Supervisor Sekolah by Username Mahasiswa and Id Laporan
    path('supervisor-sekolah/laporan-akhir-mahasiswa/nilai/<str:username>/<str:id>/',
        views.UserSupervisorSekolahNilaiLaporanAkhirMahasiswaView.as_view(),
        name='supervisor-sekolah-nilai-laporan-akhir-mahasiswa'),

    # Create template laporan borang mahasiswa
    path('supervisor-sekolah/praktikum-mahasiswa/upload-template-borang/',
        v_supv_sekolah.crud_template_laporan_borang,
        name='create-template-borang'),

    path('supervisor-sekolah/praktikum-mahasiswa/get-template-borang/',
        v_supv_sekolah.get_template_laporan_borang,
        name='get-template-borang'),

    # List Praktikum Mahasiswa by Koordinator Kuliah
    path('koordinator-kuliah/praktikum-mahasiswa/list/<str:username>/',
        views.UserKoordinatorKuliahListPraktikumMahasiswaView.as_view(),
        name='koordinator-kuliah-list-praktikum-mahasiswa'),

    # Detail Praktikum Mahasiswa Koordinator Kuliah by Username Mahasiswa and Id Laporan
    path('koordinator-kuliah/laporan-mingguan-mahasiswa/detail/<str:username>/<str:id>/',
        views.UserKoordinatorKuliahDetailLaporanMingguanMahasiswaView.as_view(),
        name='koordinator-kuliah-detail-laporan-mingguan-mahasiswa'),

    # Detail Laporan Akhir Mahasiswa Koordinator Kuliah by Username Mahasiswa and Id Laporan
    path('koordinator-kuliah/laporan-akhir-mahasiswa/detail/<str:username>/<str:id>/',
        views.UserKoordinatorKuliahDetailLaporanAkhirMahasiswaView.as_view(),
        name='koordinator-kuliah-detail-laporan-akhir-mahasiswa'),

    # Detail Borang Mahasiswa Koordinator Kuliah by Username Mahasiswa and Id Laporan
    path('koordinator-kuliah/borang-mahasiswa/detail/<str:username>/<str:id>/',
        views.UserKoordinatorKuliahDetailBorangMahasiswaView.as_view(),
        name='koordinator-kuliah-detail-borang-mahasiswa'),

    # Administrator User View Statistik Lembaga
    path('administrator/statistik-lembaga',
        views_riwayat.get_statistik_lembaga,
        name='administrator-statistik'),

    # Administrator User View Detail Mahasiswa
    path('administrator/kelola-user/detail/mahasiswa/<str:username>/',
        views.UserAdministratorKelolaUserDetailUserMahasiswaView.as_view(),
        name='administrator-detail-user-mahasiswa'),

    # Administrator User Edit Detail Mahasiswa
    path('administrator/kelola-user/edit/mahasiswa/<str:username>/',
        views.UserAdministratorKelolaUserEditUserMahasiswaView.as_view(),
        name='administrator-edit-user-mahasiswa'),

    # Administrator Get All User Mahasiswa
    path('administrator/kelola-user/list/mahasiswa/',
        views.UserAdministratorGetAllUserMahasiswaView.as_view(),
        name='administrator-get-all-user-mahasiswa'),

    # Administrator User Detail Supervisor Sekolah
    path('administrator/kelola-user/detail/supervisor-sekolah/<str:username>/',
        views.UserAdministratorKelolaUserDetailUserSupervisorSekolahView.as_view(),
        name='administrator-detail-user-supervisor-sekolah'),

    # Administrator User Edit Detail Supervisor Sekolah
    path('administrator/kelola-user/edit/supervisor-sekolah/<str:username>/',
        views.UserAdministratorKelolaUserEditUserSupervisorSekolahView.as_view(),
        name='administrator-edit-user-supervisor-sekolah'),

    # Administrator Get All User Supervisor Lembaga
    path('administrator/kelola-user/list/supervisor-sekolah/',
        views.UserAdministratorGetAllUserSupervisorSekolahView.as_view(),
        name='administrator-get-all-user-supervisor-lembaga'),

    # Administrator User Detail Supervisor Lembaga
    path('administrator/kelola-user/detail/supervisor-lembaga/<str:username>/',
        views.UserAdministratorKelolaUserDetailUserSupervisorLembagaView.as_view(),
        name='administrator-detail-user-supervisor-lembaga'),

    # Administrator User Edit Detail Supervisor Lembaga
    path('administrator/kelola-user/edit/supervisor-lembaga/<str:username>/',
        views.UserAdministratorKelolaUserEditUserSupervisorLembagaView.as_view(),
        name='administrator-edit-user-supervisor-lembaga'),

    # Administrator User Detail Koordinator Kuliah
    path('administrator/kelola-user/detail/koordinator-kuliah/<str:username>/',
        views.UserAdministratorKelolaUserDetailUserKoordinatorKuliahView.as_view(),
        name='administrator-detail-user-koordinator-kuliah'),

    # Administrator User Edit Detail Koordinator Kuliah
    path('administrator/kelola-user/edit/koordinator-kuliah/<str:username>/',
        views.UserAdministratorKelolaUserEditUserKoordinatorKuliahView.as_view(),
        name='administrator-edit-user-koordinator-kuliah'),

    # Administrator User Detail Administrator
    path('administrator/kelola-user/detail/administrator/<str:username>/',
        views.UserAdministratorKelolaUserDetailUserAdministratorView.as_view(),
        name='administrator-detail-user-administrator'),

    # Administrator User Edit Detail Administrator
    path('administrator/kelola-user/edit/administrator/<str:username>/',
        views.UserAdministratorKelolaUserEditUserAdministratorView.as_view(),
        name='administrator-edit-user-administrator'),

    # Administrator Upload All Mahasiswa Data From Excel
    path('administrator/kelola-user/mahasiswa/upload/excel/',
        views.InputDataMahasiswaExcelView.as_view(),
        name='administrator-kelola-user-mahasiswa-upload-excel'),

    # Administrator Upload All Dosen Data From Excel
    path('administrator/kelola-user/dosen/upload/excel/',
        views.InputDataDosenExcelView.as_view(),
        name='administrator-kelola-user-dosen-upload-excel'),

    path('laporan-akhir-db/',
        views.LaporanAkhirDBView.as_view(),
        name='laporan-akhir-db'),

    path('administrator/sheet-info/',
        views.UserAdministratorFileUploadInfo.as_view(),
        name='sheet-info'),

    path('mahasiswa',
        views.MahasiswaView.as_view({'get': 'list'}),
        name='mahasiswa'),

    path('periode',
        views_riwayat.get_periode_list,
        name='periode'),

]

# temp for sprint review
router = routers.DefaultRouter()
router.register('mahasiswa_praktikum', MahasiswaPraktikumView, basename="lembaga")
router.register('laporan-akhir', views.LaporanAkhirPraktikumView, basename="laporan-akhir")
router.register('mahasiswa', views.MahasiswaView, basename="mahasiswa")
urlpatterns.append(path('', include(router.urls)))
