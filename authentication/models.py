from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django_cas_ng.signals import cas_user_authenticated
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager, User
from django.contrib.auth.validators import UnicodeUsernameValidator
from .role import Role
from django.http import HttpResponseRedirect

from lembaga.models import Lembaga

import json
import random

LANG = settings.SSO_UI_ORG_DETAIL_LANG
ORG_CODE = {}
with open(settings.SSO_UI_ORG_DETAIL_FILE_PATH, 'r') as ORG_CODE_FILE:
    ORG_CODE.update(json.load(ORG_CODE_FILE))


class Role(models.Model):
    """User Profile Supervisor Sekolah model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    role = models.CharField('role', max_length=150, blank=True)

    class Meta:
        verbose_name = 'role'
        verbose_name_plural = 'role'

    def __str__(self):
        """Return username of the user."""
        return self.user.username


class SupervisorSekolah(models.Model):
    """User Profile Supervisor Sekolah model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supervisor_sekolah')
    nip = models.CharField('nip', max_length=12, blank=True)

    class Meta:
        verbose_name = 'supervisor_sekolah'
        verbose_name_plural = 'supervisor_sekolah'

    def __str__(self):
        """Return username of the user."""
        return self.user.username

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            user = User.objects.get(username=self)
            Role.objects.create(
                user=user,
                role='Supervisor Sekolah'
            )


class SupervisorLembaga(models.Model):
    """User Profile Supervisor Lembaga model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supervisor_lembaga')
    lembaga = models.ForeignKey(Lembaga, related_name="supervisor_lembaga", \
                                on_delete=models.CASCADE, default="Tidak ada lembaga")
    jabatan = models.CharField('jabatan', max_length=150, blank=False)

    class Meta:
        verbose_name = 'supervisor_lembaga'
        verbose_name_plural = 'supervisor_lembaga'

    def __str__(self):
        """Return username of the user."""
        return self.user.username

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            user = User.objects.get(username=self)
            Role.objects.create(
                user=user,
                role='Supervisor Lembaga'
            )


class Administrator(models.Model):
    """User Profile Supervisor Sekolah model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrator')
    nip = models.CharField('nip', max_length=12, blank=False)

    class Meta:
        verbose_name = 'administrator'
        verbose_name_plural = 'administrator'

    def __str__(self):
        """Return username of the user."""
        return self.user.username

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            user = User.objects.get(username=self)
            Role.objects.create(
                user=user,
                role='Administrator'
            )


class Periode(models.Model):
    """Periode model for Mahasiswa model."""

    nama = models.CharField('nama', max_length=50, blank=False)

    class Meta:
        verbose_name = 'periode'
        verbose_name_plural = 'periode'

    def __str__(self):
        """Return periode's name of the periode."""
        return self.nama


class Mahasiswa(models.Model):
    """User Profile Mahasiswa model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mahasiswa')
    org_code = models.CharField('organization_code', max_length=11, blank=True)
    npm = models.CharField('npm', max_length=10, blank=True)
    faculty = models.CharField('faculty', max_length=128, blank=True)
    major = models.CharField('major', max_length=128, blank=True)
    program = models.CharField('program', max_length=128, blank=True)
    periode = models.ForeignKey(Periode, related_name="periode", on_delete=models.CASCADE, null=True, blank=True)
    supervisor_sekolah = models.ForeignKey(SupervisorSekolah, related_name='mahasiswa', \
                                           to_field='user', on_delete=models.CASCADE, null=True, blank=True)
    supervisor_lembaga = models.ForeignKey(SupervisorLembaga, related_name='mahasiswa',\
                                           to_field='user', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'mahasiswa'
        verbose_name_plural = 'mahasiswa'

    def __str__(self):
        """Return username of the user."""
        return self.user.username

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            user = User.objects.get(username=self)
            Role.objects.create(
                user=user,
                role='Mahasiswa'
            )


class KoordinatorKuliah(models.Model):
    """User Profile Kordinator Kuliah model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='koordinator_kuliah')
    nip = models.CharField('nip', max_length=12, blank=False)

    class Meta:
        verbose_name = 'koordinator_kuliah'
        verbose_name_plural = 'koordinator_kuliah'

    def __str__(self):
        """Return username of the user."""
        return self.user.username

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            user = User.objects.get(username=self)
            Role.objects.create(
                user=user,
                role='Koordinator Praktikum'
            )


class Config(models.Model):
    """User Profile Kordinator Kuliah model."""

    key = models.CharField('key', max_length=200, blank=False)
    value = models.CharField('key', max_length=200)

    class Meta:
        verbose_name = 'config'
        verbose_name_plural = 'configs'

    def __str__(self):
        """Return username of the user."""
        return self.key
