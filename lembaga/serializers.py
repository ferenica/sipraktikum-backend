from rest_framework import serializers
from lembaga.models import Lembaga, Institusi, Tema, ErrorMessage
from rest_framework.exceptions import NotFound
from drf_extra_fields.fields import Base64ImageField


class InstitusiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institusi
        fields = '__all__'
        extra_kwargs = {
            'nama': {'validators': []},
        }


class TemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tema
        fields = '__all__'
        extra_kwargs = {
            'nama': {'validators': []},
        }


class LembagaSerializer(serializers.ModelSerializer):
    tema = TemaSerializer()
    institusi = InstitusiSerializer()

    class Meta:
        model = Lembaga
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        nama = validated_data.pop('nama')
        jenis_pelayanan = validated_data.pop('jenis_pelayanan')
        deskripsi_singkat = validated_data.pop('deskripsi_singkat')
        praktikum_ke = validated_data.pop('praktikum_ke')
        beneficaries = validated_data.pop('beneficaries')
        alamat = validated_data.pop('alamat')

        nama_tema = validated_data.pop('tema')['nama']

        error = ErrorMessage

        try:
            tema = Tema.objects.get(nama=nama_tema)
        except Tema.DoesNotExist:
            raise NotFound(detail="Tema dengan nama " + str(nama_tema) + ErrorMessage.not_found(error))

        nama_institusi = validated_data.pop('institusi')['nama']
        try:
            institusi = Institusi.objects.get(nama=nama_institusi)
        except Institusi.DoesNotExist:
            raise NotFound(detail="Institusi dengan nama " + str(nama_institusi) + ErrorMessage.not_found(error))

        lembaga = Lembaga()
        lembaga.nama = nama
        lembaga.jenis_pelayanan = jenis_pelayanan
        lembaga.deskripsi_singkat = deskripsi_singkat
        lembaga.institusi = institusi
        lembaga.tema = tema
        lembaga.praktikum_ke = praktikum_ke
        lembaga.beneficaries = beneficaries
        lembaga.alamat = alamat

        lembaga.save()

        return lembaga

    def update(self, lembaga, validated_data):
        nama = validated_data.pop('nama')
        jenis_pelayanan = validated_data.pop('jenis_pelayanan')
        deskripsi_singkat = validated_data.pop('deskripsi_singkat')
        praktikum_ke = validated_data.pop('praktikum_ke')
        beneficaries = validated_data.pop('beneficaries')
        alamat = validated_data.pop('alamat')
        last_praktikum = validated_data.pop('last_praktikum')

        nama_tema = validated_data.pop('tema')['nama']

        error = ErrorMessage
        try:
            tema = Tema.objects.get(nama=nama_tema)
        except Tema.DoesNotExist:
            raise NotFound(detail="Tema dengan nama " + str(nama_tema) + ErrorMessage.not_found(error))

        nama_institusi = validated_data.pop('institusi')['nama']
        try:
            institusi = Institusi.objects.get(nama=nama_institusi)
        except Institusi.DoesNotExist:
            raise NotFound(detail="Institusi dengan nama " + str(nama_institusi) + ErrorMessage.not_found(error))

        lembaga.nama = nama
        lembaga.jenis_pelayanan = jenis_pelayanan
        lembaga.deskripsi_singkat = deskripsi_singkat
        lembaga.institusi = institusi
        lembaga.tema = tema
        lembaga.praktikum_ke = praktikum_ke
        lembaga.beneficaries = beneficaries
        lembaga.alamat = alamat
        lembaga.last_praktikum = last_praktikum

        lembaga.save()

        return lembaga
