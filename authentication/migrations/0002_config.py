# Generated by Django 3.0.3 on 2020-06-07 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=200, verbose_name='key')),
                ('value', models.CharField(max_length=200, verbose_name='key')),
            ],
            options={
                'verbose_name': 'config',
                'verbose_name_plural': 'configs',
            },
        ),
    ]
