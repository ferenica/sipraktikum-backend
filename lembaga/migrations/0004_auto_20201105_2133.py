# Generated by Django 3.0.3 on 2020-11-05 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lembaga', '0003_carousel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Carousel',
        ),
        migrations.RemoveField(
            model_name='lembaga',
            name='gambar',
        ),
    ]