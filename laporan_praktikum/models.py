from django.db import models
from lembaga.models import Lembaga
from authentication.models import Administrator, KoordinatorKuliah, Mahasiswa, \
    SupervisorLembaga, SupervisorSekolah
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import uuid

import os


def dir_path_template_borang(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>

    if instance.t_borang_supv_sekolah:
        return '{0}/{1}/{2}'.format(str(instance.supervisor_sekolah), 't_borang_supv_sekolah', filename)

    if instance.t_borang_supv_lembaga:
        return '{0}/{1}/{2}'.format(str(instance.supervisor_sekolah), 't_borang_supv_lembaga', filename)

    if instance.t_borang_supv_perkuliahan:
        return '{0}/{1}/{2}'.format(str(instance.supervisor_sekolah), 't_borang_supv_perkuliahan', filename)

# For model LaporanAkhirPraktikum and LaporanBorangPraktikum to spesific media path


def dir_path_generator(instance, filename):
    if instance.laporan_akhir:
        return '{0}/{1}/{2}'.format(str(instance.mahasiswa), 'laporan_akhir', filename)

    if instance.profil_lembaga:
        return '{0}/{1}/{2}'.format(str(instance.mahasiswa), 'profil_lembaga', filename)

    if instance.borang_supv_sekolah:
        return '{0}/{1}/{2}'.format(str(instance.mahasiswa), 'borang_supv_sekolah', filename)

    if instance.borang_supv_lembaga:
        return '{0}/{1}/{2}'.format(str(instance.mahasiswa), 'borang_supv_lembaga', filename)

    if instance.borang_supv_perkuliahan:
        return '{0}/{1}/{2}'.format(str(instance.mahasiswa), 'borang_supv_perkuliahan', filename)


class OverwriteStorage(FileSystemStorage):
    '''
    Changes Django's default behavior and makes it overwrite
    same name that were loaded by the user instead of renaming them.

    '''

    def get_available_name(self, filename, max_length=None):
        temp_filename = filename
        if self.exists(filename):
            os.remove(os.path.join(settings.MEDIA_ROOT, filename))
        return filename


class Praktikum(models.Model):
    jenis_praktikum = models.CharField(max_length=255, unique=True, default="Praktikum 1")

    def __str__(self):
        return self.jenis_praktikum


class MahasiswaPraktikum(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, to_field="user", related_name="mahasiswa_praktikum", \
                             on_delete=models.CASCADE)
    list_praktikum = models.ForeignKey(Praktikum, to_field="jenis_praktikum", related_name="mahasiswa_praktikum", \
                                       on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


class AttributeLaporanPraktikum(models.Model):
    '''
    Abstract Class
    '''
    nama_laporan = models.CharField(max_length=255)
    waktu_deadline = models.DateTimeField(blank=True, null=True)  # unggah
    waktu_submisi = models.DateTimeField(blank=True, null=True)
    waktu_nilai_supv_sekolah = models.DateTimeField(blank=True, null=True)  # supv sekolah nilai
    waktu_nilai_supv_lembaga = models.DateTimeField(blank=True, null=True)  # supv lembaga nilai

    status_publikasi = models.BooleanField(default=False)
    status_submisi = models.BooleanField(default=False)
    skor_laporan_sekolah = models.IntegerField(default=-1)
    skor_laporan_lembaga = models.IntegerField(default=-1)

    class Meta:
        abstract = True


class KelolaLaporanPraktikum(AttributeLaporanPraktikum):
    '''
    Laporan Mingguan Praktikum
    '''
    mahasiswa = models.ForeignKey(Mahasiswa, to_field="user", related_name="kelola_laporan", \
                                  on_delete=models.CASCADE)
    jenis_praktikum = models.ForeignKey(Praktikum, to_field="jenis_praktikum", related_name="kelola_laporan", \
                                  on_delete=models.CASCADE)
    link_submisi = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):  # pragma: no cover
        return self.nama_laporan


class LaporanAkhirPraktikum(AttributeLaporanPraktikum):
    '''
    Laporan Akhir Praktikum
    '''
    mahasiswa = models.ForeignKey(Mahasiswa, to_field="user", related_name="laporan_akhir", \
                                  on_delete=models.CASCADE)
    jenis_praktikum = models.ForeignKey(Praktikum, to_field="jenis_praktikum", related_name="laporan_akhir", \
                                  on_delete=models.CASCADE)
    lembaga = models.ForeignKey(Lembaga, related_name="laporan_akhir_set_lembaga",
                                blank=True,
                                null=True,
                                default=None,
                                on_delete=models.CASCADE)
    periode_praktikum = models.CharField(max_length=50, blank=True, default=" ")
    laporan_akhir = models.FileField(blank=True, null=True)
    profil_lembaga = models.FileField(blank=True, null=True)
    umpan_balik = models.CharField(max_length=255, blank=True, default=" ")

    def getLembagaID(self):
        return self.lembaga.id

    def updateTahun(self):
        currentYear = self.lembaga.last_praktikum
        newYear = self.periode_praktikum[:4]
        if newYear != '' and (currentYear == None or currentYear < int(newYear)):
            return newYear

        else:
            return currentYear
    
    def save(self, *args, **kwargs):
        Lembaga.objects.filter(id = self.getLembagaID()).update(last_praktikum = self.updateTahun())
        super().save(*args,**kwargs)

    def __str__(self):  # pragma: no cover
        return self.nama_laporan


class LaporanBorangPraktikum(AttributeLaporanPraktikum):
    '''
    Laporan Borang Praktikum
    '''
    mahasiswa = models.ForeignKey(Mahasiswa, to_field="user", related_name="laporan_borang", \
                                  on_delete=models.CASCADE)
    jenis_praktikum = models.ForeignKey(Praktikum, to_field="jenis_praktikum", related_name="laporan_borang", \
                                  on_delete=models.CASCADE)
    borang_supv_sekolah = models.FileField(blank=True, null=True)
    borang_supv_lembaga = models.FileField(blank=True, null=True)
    borang_supv_perkuliahan = models.FileField(blank=True, null=True)

    def __str__(self):  # pragma: no cover
        return self.nama_laporan


# flake8: noqa
class TemplateBorangPenilaianPraktikum(models.Model):
    supervisor_sekolah = models.ForeignKey(SupervisorSekolah, related_name='template_borang', \
                                           to_field='user', on_delete=models.CASCADE, null=True, blank=True)

    t_borang_supv_sekolah = models.FileField(blank=True, null=True, upload_to=dir_path_template_borang)
    t_borang_supv_lembaga = models.FileField(blank=True, null=True, upload_to=dir_path_template_borang)
    t_borang_supv_perkuliahan = models.FileField(blank=True, null=True, upload_to=dir_path_template_borang)

    def __str__(self):  # pragma: no cover
        return '{}'.format(self.supervisor_sekolah.__str__())
