# Generated by Django 3.0.3 on 2020-06-03 14:51

from django.db import migrations, models
import laporan_praktikum.models


class Migration(migrations.Migration):

    dependencies = [
        ('laporan_praktikum', '0002_auto_20200603_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laporanborangpraktikum',
            name='borang_supv_lembaga',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='laporanborangpraktikum',
            name='borang_supv_perkuliahan',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='laporanborangpraktikum',
            name='borang_supv_sekolah',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='templateborangpenilaianpraktikum',
            name='t_borang_supv_lembaga',
            field=models.FileField(blank=True, null=True, storage=laporan_praktikum.models.OverwriteStorage,
                                   upload_to=laporan_praktikum.models.dir_path_template_borang),
        ),
        migrations.AlterField(
            model_name='templateborangpenilaianpraktikum',
            name='t_borang_supv_perkuliahan',
            field=models.FileField(blank=True, null=True, storage=laporan_praktikum.models.OverwriteStorage,
                                   upload_to=laporan_praktikum.models.dir_path_template_borang),
        ),
        migrations.AlterField(
            model_name='templateborangpenilaianpraktikum',
            name='t_borang_supv_sekolah',
            field=models.FileField(blank=True, null=True, storage=laporan_praktikum.models.OverwriteStorage,
                                   upload_to=laporan_praktikum.models.dir_path_template_borang),
        ),
    ]
