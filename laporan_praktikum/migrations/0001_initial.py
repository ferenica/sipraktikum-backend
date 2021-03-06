# Generated by Django 3.0.3 on 2020-06-03 12:43

from django.db import migrations, models
import django.db.models.deletion
import laporan_praktikum.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('lembaga', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Praktikum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis_praktikum', models.CharField(default='Praktikum 1', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TemplateBorangPenilaianPraktikum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_borang_supv_sekolah', models.FileField(blank=True, null=True, upload_to=laporan_praktikum.models.dir_path_template_borang)),
                ('t_borang_supv_lembaga', models.FileField(blank=True, null=True, upload_to=laporan_praktikum.models.dir_path_template_borang)),
                ('t_borang_supv_perkuliahan', models.FileField(blank=True, null=True, upload_to=laporan_praktikum.models.dir_path_template_borang)),
                ('supervisor_sekolah', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='template_borang', to='authentication.SupervisorSekolah', to_field='user')),
            ],
        ),
        migrations.CreateModel(
            name='MahasiswaPraktikum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('list_praktikum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mahasiswa_praktikum', to='laporan_praktikum.Praktikum', to_field='jenis_praktikum')),
                ('mahasiswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mahasiswa_praktikum', to='authentication.Mahasiswa', to_field='user')),
            ],
        ),
        migrations.CreateModel(
            name='LaporanBorangPraktikum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_laporan', models.CharField(max_length=255)),
                ('waktu_deadline', models.DateTimeField(blank=True, null=True)),
                ('waktu_submisi', models.DateTimeField(blank=True, null=True)),
                ('waktu_nilai_supv_sekolah', models.DateTimeField(blank=True, null=True)),
                ('waktu_nilai_supv_lembaga', models.DateTimeField(blank=True, null=True)),
                ('status_publikasi', models.BooleanField(default=False)),
                ('status_submisi', models.BooleanField(default=False)),
                ('skor_laporan_sekolah', models.IntegerField(default=-1)),
                ('skor_laporan_lembaga', models.IntegerField(default=-1)),
                ('borang_supv_sekolah', models.FileField(blank=True, null=True, upload_to='')),
                ('borang_supv_lembaga', models.FileField(blank=True, null=True, upload_to='')),
                ('borang_supv_perkuliahan', models.FileField(blank=True, null=True, upload_to='')),
                ('jenis_praktikum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='laporan_borang', to='laporan_praktikum.Praktikum', to_field='jenis_praktikum')),
                ('mahasiswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='laporan_borang', to='authentication.Mahasiswa', to_field='user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LaporanAkhirPraktikum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_laporan', models.CharField(max_length=255)),
                ('waktu_deadline', models.DateTimeField(blank=True, null=True)),
                ('waktu_submisi', models.DateTimeField(blank=True, null=True)),
                ('waktu_nilai_supv_sekolah', models.DateTimeField(blank=True, null=True)),
                ('waktu_nilai_supv_lembaga', models.DateTimeField(blank=True, null=True)),
                ('status_publikasi', models.BooleanField(default=False)),
                ('status_submisi', models.BooleanField(default=False)),
                ('skor_laporan_sekolah', models.IntegerField(default=-1)),
                ('skor_laporan_lembaga', models.IntegerField(default=-1)),
                ('periode_praktikum', models.CharField(blank=True, default=' ', max_length=50)),
                ('laporan_akhir', models.FileField(blank=True, null=True, upload_to='')),
                ('profil_lembaga', models.FileField(blank=True, null=True, upload_to='')),
                ('umpan_balik', models.CharField(blank=True, default=' ', max_length=255)),
                ('jenis_praktikum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='laporan_akhir', to='laporan_praktikum.Praktikum', to_field='jenis_praktikum')),
                ('lembaga', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='laporan_akhir_set_lembaga', to='lembaga.Lembaga')),
                ('mahasiswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='laporan_akhir', to='authentication.Mahasiswa', to_field='user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KelolaLaporanPraktikum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_laporan', models.CharField(max_length=255)),
                ('waktu_deadline', models.DateTimeField(blank=True, null=True)),
                ('waktu_submisi', models.DateTimeField(blank=True, null=True)),
                ('waktu_nilai_supv_sekolah', models.DateTimeField(blank=True, null=True)),
                ('waktu_nilai_supv_lembaga', models.DateTimeField(blank=True, null=True)),
                ('status_publikasi', models.BooleanField(default=False)),
                ('status_submisi', models.BooleanField(default=False)),
                ('skor_laporan_sekolah', models.IntegerField(default=-1)),
                ('skor_laporan_lembaga', models.IntegerField(default=-1)),
                ('link_submisi', models.URLField(blank=True, max_length=255, null=True)),
                ('jenis_praktikum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kelola_laporan', to='laporan_praktikum.Praktikum', to_field='jenis_praktikum')),
                ('mahasiswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kelola_laporan', to='authentication.Mahasiswa', to_field='user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
