# Generated by Django 3.1.3 on 2021-03-25 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lembaga', '0004_auto_20201105_2133'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
