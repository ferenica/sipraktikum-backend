from .models import (
    Mahasiswa,
    SupervisorSekolah,
    SupervisorLembaga,
    KoordinatorKuliah,
    Administrator,
    User,
    Periode,
    Config,
    Role
)
from django.contrib import admin


"""Profile model admin class."""


@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    pass


"""Profile model admin class."""


@admin.register(SupervisorSekolah)
class SupervisorSekolahAdmin(admin.ModelAdmin):
    pass


"""Profile model admin class."""


@admin.register(KoordinatorKuliah)
class KoordinatorKuliahAdmin(admin.ModelAdmin):
    pass


"""Profile model admin class."""


@admin.register(SupervisorLembaga)
class SupervisorLembagaAdmin(admin.ModelAdmin):
    pass


"""Profile model admin class."""


@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    pass


@admin.register(Periode)
class PeriodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    pass


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass
