# Generated by Django 3.1.3 on 2021-06-06 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lembaga', '0008_remove_lembaga_last_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='lembaga',
            name='last_praktikum',
            field=models.IntegerField(blank=True, null=True, verbose_name='last activity'),
        ),
    ]
