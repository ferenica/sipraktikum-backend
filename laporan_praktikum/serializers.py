from django.db import models
from rest_framework import serializers
from lembaga.models import Lembaga
from lembaga.serializers import LembagaSerializer
from authentication.models import (
    Mahasiswa,
    SupervisorLembaga,
    SupervisorSekolah,
    KoordinatorKuliah,
    Administrator,
    User
)
from authentication.serializers import (
    UserSerializer,
    SupervisorSekolahSerializer,
    SupervisorLembagaSerializer,
    MahasiswaSerializer,
)
from laporan_praktikum.models import (
    Praktikum,
    MahasiswaPraktikum,
    KelolaLaporanPraktikum,
    LaporanAkhirPraktikum,
    LaporanBorangPraktikum,
    TemplateBorangPenilaianPraktikum
)


date_format = "%d-%m-%Y %H:%M"


class PraktikumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Praktikum
        fields = ['id', 'jenis_praktikum']


class SupervisorLembagaSpesificSerializer(serializers.ModelSerializer):
    """Supervisor Lembaga serializer json field."""
    user = UserSerializer()

    class Meta:
        model = SupervisorLembaga
        fields = ['user']


class SupervisorLembagaUsernameSerializer(serializers.ModelSerializer):
    """Supervisor Lembaga serializer json field."""

    class Meta:
        model = User
        fields = ['username', 'last_login', 'is_active']


class MahasiswaWithJenisPraktikumSerializer(MahasiswaSerializer):

    jenis_praktikum = serializers.SerializerMethodField()
    status_kelola = serializers.SerializerMethodField()

    def get_jenis_praktikum(self, obj_mahasiswa):
        mahasiswa_praktikum = MahasiswaPraktikum.objects.filter(mahasiswa=obj_mahasiswa, status=True)
        if len(mahasiswa_praktikum) > 0:
            mahasiswa_praktikum = mahasiswa_praktikum[0].list_praktikum
        else:
            mahasiswa_praktikum = ""
        return str(mahasiswa_praktikum)

    def get_status_kelola(self, obj_mahasiswa):
        status = False
        list_praktikum_mingguan = KelolaLaporanPraktikum.objects.filter(mahasiswa=obj_mahasiswa, status_publikasi=True).count()
        list_praktikum_akhir = LaporanAkhirPraktikum.objects.filter(mahasiswa=obj_mahasiswa, status_publikasi=True).count()
        list_praktikum_borang = LaporanBorangPraktikum.objects.filter(mahasiswa=obj_mahasiswa, status_publikasi=True).count()

        if list_praktikum_mingguan != 0 or list_praktikum_akhir != 0 or list_praktikum_borang != 0:
            status = True

        return status

    class Meta(MahasiswaSerializer.Meta):
        model = Mahasiswa
        fields = ['jenis_praktikum', 'status_kelola'] + MahasiswaSerializer.Meta.fields


class SupervisorSekolahListMahasiswaSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    mahasiswa = MahasiswaWithJenisPraktikumSerializer(many=True)

    class Meta:
        model = SupervisorSekolah
        fields = [
            'user',
            'nip',
            'mahasiswa'
        ]


class MahasiswaPraktikumSerializer(serializers.ModelSerializer):

    class Meta:
        model = MahasiswaPraktikum
        fields = ['mahasiswa', 'list_praktikum', 'status']


class SupervisorLembagaListMahasiswaSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    mahasiswa = MahasiswaWithJenisPraktikumSerializer(many=True)
    lembaga = LembagaSerializer()

    class Meta:
        model = SupervisorLembaga
        fields = [
            'user',
            'lembaga',
            'jabatan',
            'mahasiswa'
        ]


###################################
# Basic Riwayat Serializer Class ##
###################################


class RiwayatKelolaLaporanPraktikumSerializer_v2(serializers.ModelSerializer):

    class Meta:
        model = KelolaLaporanPraktikum
        fields = ['id', 'jenis_praktikum', 'nama_laporan']


class RiwayatLaporanAkhirPraktikumSerializer_v2(serializers.ModelSerializer):

    class Meta:
        model = LaporanAkhirPraktikum
        fields = ['id', 'jenis_praktikum', 'nama_laporan']


class RiwayatLaporanBorangPraktikumSerializer_v2(serializers.ModelSerializer):

    class Meta:
        model = LaporanBorangPraktikum
        fields = ['id', 'jenis_praktikum', 'nama_laporan']

#####################################
# SERIALIZER RIWAYAT DARI MAHASISWA #
#####################################


class MahasiswaWithContextProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Mahasiswa
        fields = ['user']


class RiwayatSupervisiMahasiswaWithContextProfileSerializer(serializers.ModelSerializer):
    mahasiswa = MahasiswaWithContextProfileSerializer()

    class Meta:
        model = KelolaLaporanPraktikum
        fields = '__all__'


class RiwayatSupervisiMahasiswaLaporanAkhirWithContextProfileSerializer(serializers.ModelSerializer):
    mahasiswa = MahasiswaWithContextProfileSerializer()

    class Meta:
        model = LaporanAkhirPraktikum
        fields = '__all__'


class RiwayatSupervisiMahasiswaLaporanBorangWithContextProfileSerializer(serializers.ModelSerializer):
    mahasiswa = MahasiswaWithContextProfileSerializer()

    class Meta:
        model = LaporanBorangPraktikum
        fields = '__all__'


class RiwayatMahasiswaLaporanMingguanSerializer(RiwayatKelolaLaporanPraktikumSerializer_v2):
    waktu_deadline = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_submisi = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta(RiwayatKelolaLaporanPraktikumSerializer_v2.Meta):
        ordering = ['-waktu_submisi']
        fields = RiwayatKelolaLaporanPraktikumSerializer_v2.Meta.fields + ['waktu_deadline', 'waktu_submisi', 'status_submisi']


class RiwayatMahasiswaLaporanAkhirSerializer(RiwayatLaporanAkhirPraktikumSerializer_v2):
    waktu_deadline = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_submisi = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta(RiwayatLaporanAkhirPraktikumSerializer_v2.Meta):
        ordering = ['-waktu_submisi']
        fields = RiwayatLaporanAkhirPraktikumSerializer_v2.Meta.fields + ['waktu_deadline', 'waktu_submisi', 'status_submisi']


class RiwayatMahasiswaLaporanBorangSerializer(RiwayatLaporanBorangPraktikumSerializer_v2):
    waktu_deadline = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_submisi = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta(RiwayatLaporanBorangPraktikumSerializer_v2.Meta):
        ordering = ['-waktu_submisi']
        fields = RiwayatLaporanBorangPraktikumSerializer_v2.Meta.fields + ['waktu_deadline', 'waktu_submisi', 'status_submisi']

##############################################
# SERIALIZER RIWAYAT DARI SUPERVISOR SEKOLAH #
##############################################


class RiwayatSupervisiMahasiswaBySupervisorSekolahSerializer(RiwayatKelolaLaporanPraktikumSerializer_v2):

    waktu_nilai_supv_sekolah = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta(RiwayatKelolaLaporanPraktikumSerializer_v2.Meta):
        ordering = ['-waktu_nilai_supv_sekolah']
        fields = RiwayatKelolaLaporanPraktikumSerializer_v2.Meta.fields + ['waktu_nilai_supv_sekolah', 'status_submisi']


class RiwayatSupervisiLaporanAkhirMahasiswaBySupervisorSekolahSerializer(RiwayatLaporanAkhirPraktikumSerializer_v2):
    mahasiswa = MahasiswaWithContextProfileSerializer()
    waktu_nilai_supv_sekolah = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta(RiwayatLaporanAkhirPraktikumSerializer_v2.Meta):
        ordering = ['-waktu_nilai_supv_sekolah']
        fields = ['mahasiswa'] + RiwayatLaporanAkhirPraktikumSerializer_v2.Meta.fields + ['waktu_nilai_supv_sekolah', 'status_submisi']


class RiwayatSupervisiLaporanBorangMahasiswaBySupervisorSekolahSerializer(RiwayatLaporanBorangPraktikumSerializer_v2):
    mahasiswa = MahasiswaWithContextProfileSerializer()
    waktu_nilai_supv_sekolah = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta(RiwayatLaporanAkhirPraktikumSerializer_v2.Meta):
        ordering = ['-waktu_nilai_supv_sekolah']
        fields = ['mahasiswa'] + RiwayatLaporanBorangPraktikumSerializer_v2.Meta.fields + ['waktu_nilai_supv_sekolah', 'status_submisi']


##############################################
# SERIALIZER RIWAYAT DARI SUPERVISOR LEMBAGA #
##############################################

class RiwayatSupervisiMahasiswaBySupervisorLembagaSerializer(RiwayatKelolaLaporanPraktikumSerializer_v2):
    waktu_nilai_supv_lembaga = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta(RiwayatKelolaLaporanPraktikumSerializer_v2.Meta):
        ordering = ['-waktu_nilai_supv_lembaga']
        fields = RiwayatKelolaLaporanPraktikumSerializer_v2.Meta.fields + ['waktu_nilai_supv_lembaga', 'status_submisi']


class RiwayatSupervisiLaporanAkhirMahasiswaBySupervisorLembagaSerializer(RiwayatLaporanAkhirPraktikumSerializer_v2):
    waktu_nilai_supv_lembaga = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta(RiwayatLaporanAkhirPraktikumSerializer_v2.Meta):
        ordering = ['-waktu_nilai_supv_lembaga']
        fields = RiwayatLaporanAkhirPraktikumSerializer_v2.Meta.fields + ['waktu_nilai_supv_lembaga', 'status_submisi']


class RiwayatSupervisiLaporanBorangMahasiswaBySupervisorLembagaSerializer(RiwayatLaporanBorangPraktikumSerializer_v2):
    waktu_nilai_supv_lembaga = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta(RiwayatLaporanBorangPraktikumSerializer_v2.Meta):
        ordering = ['-waktu_nilai_supv_lembaga']
        fields = RiwayatLaporanBorangPraktikumSerializer_v2.Meta.fields + ['waktu_nilai_supv_lembaga', 'status_submisi']

##############################


class RiwayatLaporanPraktikumMahasiswaSerializer(serializers.ModelSerializer):
    # change datetime-format
    waktu_deadline = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_submisi = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_nilai_supv_lembaga = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_nilai_supv_sekolah = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta:
        model = KelolaLaporanPraktikum
        ordering = ['-waktu_submisi', '-waktu_nilai_supv_lembaga', '-waktu_nilai_supv_sekolah']

        fields = ['id', 'jenis_praktikum', 'nama_laporan', 'waktu_deadline', 'waktu_submisi',
                'waktu_nilai_supv_sekolah', 'waktu_nilai_supv_lembaga', 'status_publikasi', 'status_submisi',
                'skor_laporan_sekolah', 'skor_laporan_lembaga', 'link_submisi']


##################################################

class KelolaLaporanPraktikumSerializer(serializers.ModelSerializer):

    # change datetime-format
    waktu_deadline = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_submisi = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_nilai_supv_lembaga = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_nilai_supv_sekolah = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta:
        model = KelolaLaporanPraktikum
        fields = ['id', 'jenis_praktikum', 'nama_laporan', 'waktu_deadline', 'waktu_submisi',
                'waktu_nilai_supv_sekolah', 'waktu_nilai_supv_lembaga', 'status_publikasi', 'status_submisi',
                'skor_laporan_sekolah', 'skor_laporan_lembaga', 'link_submisi']


class LaporanAkhirPraktikumSerializer(serializers.ModelSerializer):
    mahasiswa = MahasiswaSerializer()

    # change datetime-format
    waktu_deadline = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_submisi = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_nilai_supv_lembaga = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_nilai_supv_sekolah = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta:
        model = LaporanAkhirPraktikum
        fields = ['mahasiswa', 'id', 'jenis_praktikum', 'nama_laporan', 'waktu_deadline', 'waktu_submisi',
        'waktu_nilai_supv_sekolah', 'waktu_nilai_supv_lembaga', 'status_publikasi', 'status_submisi',
        'skor_laporan_sekolah', 'skor_laporan_lembaga', 'laporan_akhir', 'profil_lembaga', 'umpan_balik', 'periode_praktikum']


class LaporanBorangPraktikumSerializer(serializers.ModelSerializer):
    mahasiswa = MahasiswaSerializer()
    # change datetime-format
    waktu_deadline = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_submisi = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_nilai_supv_lembaga = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_nilai_supv_sekolah = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta:
        model = LaporanBorangPraktikum
        fields = ['mahasiswa', 'id', 'jenis_praktikum', 'nama_laporan', 'waktu_deadline', 'waktu_submisi',
        'waktu_nilai_supv_sekolah', 'waktu_nilai_supv_lembaga', 'status_publikasi', 'status_submisi',
        'skor_laporan_sekolah', 'skor_laporan_lembaga',
        'borang_supv_sekolah',
        'borang_supv_lembaga',
        'borang_supv_perkuliahan']


class LaporanAkhirPraktikumSerializer_v2(serializers.ModelSerializer):

    # change datetime-format
    waktu_deadline = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_submisi = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_nilai_supv_lembaga = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_nilai_supv_sekolah = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta:
        model = LaporanAkhirPraktikum
        fields = ['id', 'jenis_praktikum', 'nama_laporan', 'waktu_deadline', 'waktu_submisi',
        'waktu_nilai_supv_sekolah', 'waktu_nilai_supv_lembaga', 'status_publikasi', 'status_submisi',
        'skor_laporan_sekolah', 'skor_laporan_lembaga', 'laporan_akhir', 'profil_lembaga', 'umpan_balik', 'periode_praktikum']


class TemplateLaporanBorangPraktikumSerializer_v2(serializers.ModelSerializer):
    supervisor_sekolah = SupervisorSekolah()

    class Meta:
        model = TemplateBorangPenilaianPraktikum
        fields = ['id', 't_borang_supv_sekolah', 't_borang_supv_lembaga', 't_borang_supv_perkuliahan']


'''
class LaporanBorangPraktikumSerializer(serializers.ModelSerializer):

    # change datetime-format
    waktu_deadline = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_submisi = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_nilai_supv_lembaga = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_nilai_supv_sekolah = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta:
        model = LaporanBorangPraktikum
        fields = ['id', 'jenis_praktikum', 'nama_laporan', 'waktu_deadline', 'waktu_submisi',
        'waktu_nilai_supv_sekolah', 'waktu_nilai_supv_lembaga', 'status_publikasi', 'status_submisi',
        'skor_laporan_sekolah', 'skor_laporan_lembaga',
        'borang_supv_sekolah',
        'borang_supv_lembaga',
        'borang_supv_perkuliahan']
'''


class KelolaLaporanPraktikumDefaultSerializer(serializers.ModelSerializer):
    """
    Serializer for Kelola Laporan list
    """
    mahasiswa = MahasiswaSerializer()
    jenis_praktikum = PraktikumSerializer()

    # change datetime-format
    waktu_deadline = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_submisi = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_nilai_supv_lembaga = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    waktu_nilai_supv_sekolah = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta:
        model = KelolaLaporanPraktikum

        fields = [
            'mahasiswa',
            'id',
            'jenis_praktikum',
            'nama_laporan',
            'waktu_deadline',
            'waktu_submisi',
            'waktu_nilai_supv_sekolah',
            'waktu_nilai_supv_lembaga',
            'status_publikasi',
            'status_submisi',
            'skor_laporan_sekolah',
            'skor_laporan_lembaga',
            'link_submisi'
        ]


class MahasiswaDetailPraktikumSerializer(serializers.ModelSerializer):
    """
    Serializer for Mahasiswa Praktikum
    """
    mahasiswa = MahasiswaSerializer()
    list_praktikum = PraktikumSerializer()

    class Meta:
        model = MahasiswaPraktikum
        fields = ['mahasiswa', 'list_praktikum', 'status']


class KoordinatorKuliahListMahasiswaSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    mahasiswa = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = KoordinatorKuliah
        fields = [
            'user',
            'nip',
            'mahasiswa'
        ]

    def get_mahasiswa(self, obj):
        return MahasiswaWithJenisPraktikumSerializer(Mahasiswa.objects.all(), many=True).data


class AdministratorListUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    user_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Administrator
        fields = [
            'user',
            'nip',
            'user_list'
        ]

    def get_user_list(self, obj):
        return UserSerializer(User.objects.all(), many=True).data


class MahasiswaDetailPraktikumSerializerTemp(serializers.ModelSerializer):
    """
    Serializer for Mahasiswa Praktikum
    """
    mahasiswa = MahasiswaSerializer()

    class Meta:
        model = MahasiswaPraktikum
        fields = '__all__'
        depth = 2


'''
class LaporanAkhirPraktikumSerializer(serializers.ModelSerializer):
    mahasiswa = MahasiswaSerializer()

    class Meta:
        model = LaporanAkhirPraktikum
        fields = [
            'nama_laporan',
            'mahasiswa',
            'jenis_praktikum',
            'laporan_akhir',
            'id'
        ]
'''
