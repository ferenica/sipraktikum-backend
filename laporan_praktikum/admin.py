from django.contrib import admin
from laporan_praktikum.models import Praktikum, KelolaLaporanPraktikum, \
    MahasiswaPraktikum, LaporanAkhirPraktikum, LaporanBorangPraktikum, TemplateBorangPenilaianPraktikum


@admin.register(Praktikum)
class PraktikumAdmin(admin.ModelAdmin):
    list_display = ['id', 'jenis_praktikum']


@admin.register(MahasiswaPraktikum)
class MahasiswaPraktikumAdmin(admin.ModelAdmin):
    list_display = ['id', 'mahasiswa', 'list_praktikum', 'status']


@admin.register(KelolaLaporanPraktikum)
class KelolaLaporanPraktikumAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama_laporan', 'jenis_praktikum', 'mahasiswa', 'waktu_deadline', 'waktu_submisi',
        'waktu_nilai_supv_sekolah', 'waktu_nilai_supv_lembaga', 'status_publikasi', 'status_submisi',
        'skor_laporan_sekolah', 'skor_laporan_lembaga', 'link_submisi']


@admin.register(LaporanAkhirPraktikum)
class LaporanAkhirPraktikumAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama_laporan', 'lembaga', 'jenis_praktikum', 'mahasiswa', 'periode_praktikum',
        'waktu_deadline', 'waktu_submisi',
        'waktu_nilai_supv_sekolah', 'waktu_nilai_supv_lembaga', 'status_publikasi', 'status_submisi',
        'skor_laporan_sekolah', 'skor_laporan_lembaga', 'laporan_akhir', 'profil_lembaga', 'umpan_balik']


@admin.register(LaporanBorangPraktikum)
class LaporanBorangPraktikumAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama_laporan', 'jenis_praktikum', 'mahasiswa', 'waktu_deadline', 'waktu_submisi',
        'waktu_nilai_supv_sekolah', 'waktu_nilai_supv_lembaga', 'status_publikasi', 'status_submisi',
        'borang_supv_sekolah', 'borang_supv_lembaga', 'borang_supv_perkuliahan']


@admin.register(TemplateBorangPenilaianPraktikum)
class TemplateBorangPenilaianPraktikum(admin.ModelAdmin):
    list_display = ['id', 'supervisor_sekolah', 't_borang_supv_sekolah',
    't_borang_supv_lembaga', 't_borang_supv_perkuliahan']
