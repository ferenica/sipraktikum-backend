from django.contrib import admin
from lembaga import models

# Register your models here.
admin.site.register(models.Lembaga)
admin.site.register(models.Institusi)
admin.site.register(models.Tema)
admin.site.register(models.ErrorMessage)
