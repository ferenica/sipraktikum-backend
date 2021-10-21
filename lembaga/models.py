""" This module create a models """
from django.db import models
from django.conf import settings
import os


class Institusi(models.Model):
    """ Models for Institusi """
    nama = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nama


class Tema(models.Model):
    """ Models for Tema """
    nama = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nama


def upload_location(instance, filename):
    _, extension = filename.split('.')
    return '%s.%s' % (instance.nama, extension)


class Lembaga(models.Model):
    """ Models for Lembaga """
    nama = models.CharField(max_length=255)
    jenis_pelayanan = models.CharField(max_length=255)
    institusi = models.ForeignKey(Institusi, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    deskripsi_singkat = models.TextField()
    beneficaries = models.CharField(max_length=1024)
    alamat = models.CharField(max_length=1024)
    praktikum_ke = models.IntegerField()
    last_praktikum = models.IntegerField('last activity', blank=True, null=True)

    def __str__(self):
        return self.nama


class ErrorMessage(models.Model):
    """ Models for Error Messages """
    def not_found(self):
        return "tidak ditemukan"
