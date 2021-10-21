""" This module test the functionality of the module """

from django.test import TestCase
from .models import Lembaga, Tema, Institusi
from .serializers import LembagaSerializer, InstitusiSerializer, TemaSerializer
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.views import status
from rest_framework.exceptions import NotFound
from lembaga.views import LembagaView
from django.core.files import File
from io import BytesIO
from PIL import Image
import base64
import pytest


# Create your tests here.
class BaseViewTest(APITestCase):
    client = APIClient()

    def get_image_file(self, name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        tema = Tema.objects.create(nama="test_tema")
        institusi = Institusi.objects.create(nama="test_institusi")
        lembaga1 = Lembaga.objects.create(nama="test_nama",
                                          jenis_pelayanan="test_pelayanan",
                                          deskripsi_singkat="test_deskripsi",
                                          tema=tema, institusi=institusi,
                                          praktikum_ke=1, beneficaries="test_beneficaries",
                                          alamat="test_alamat")
        lembaga1.gambar = self.get_image_file()
        lembaga1.save()
        lembaga2 = Lembaga.objects.create(nama="test_nama1",
                                          jenis_pelayanan="test_pelayanan",
                                          deskripsi_singkat="test_deskripsi",
                                          tema=tema, institusi=institusi,
                                          praktikum_ke=1, beneficaries="test_beneficaries",
                                          alamat="test_alamat")
        lembaga2.gambar = self.get_image_file()
        lembaga2.save()
        lembaga3 = Lembaga.objects.create(nama="test_nama2",
                                          jenis_pelayanan="test_pelayanan",
                                          deskripsi_singkat="test_deskripsi",
                                          tema=tema, institusi=institusi,
                                          praktikum_ke=1, beneficaries="test_beneficaries",
                                          alamat="test_alamat")
        lembaga3.gambar = self.get_image_file()
        lembaga3.save()


class LembagaFunctionality(BaseViewTest):

    def test_lembaga_str(self):
        """ Test Models Lembaga Field """
        test_lembaga = Lembaga.objects.get(nama="test_nama")
        tema = Tema.objects.get(nama="test_tema")
        institusi = Institusi.objects.get(nama="test_institusi")
        self.assertEqual(str(test_lembaga), 'test_nama')
        self.assertEqual(test_lembaga.jenis_pelayanan, 'test_pelayanan')
        self.assertEqual(test_lembaga.deskripsi_singkat, 'test_deskripsi')
        self.assertEqual(test_lembaga.praktikum_ke, 1)
        self.assertEqual(test_lembaga.alamat, "test_alamat")
        self.assertEqual(test_lembaga.beneficaries, "test_beneficaries")
        self.assertEqual(str(test_lembaga.tema), str(tema))
        self.assertEqual(str(test_lembaga.institusi), str(institusi))

    def test_tema_not_found(self):
        with pytest.raises(Tema.DoesNotExist):
            tema = Tema.objects.get(nama="tema")
            self.assertRaises(NotFound, tema)

    def test_institusi_not_found(self):
        with pytest.raises(Institusi.DoesNotExist):
            institusi = Institusi.objects.get(nama="institusi")
            self.assertRaises(NotFound, institusi)

    def test_upload_location(self):
        nama = "test1"
        filename = "test.pdf"
        _, extension = filename.split('.')
        self.assertEqual('%s.%s' % (nama, extension), "test1.pdf")

    def test_get_all_lembaga(self):
        """
        Test get all lembaga API functionality
        """
        factory = APIRequestFactory()
        request = factory.get('/api/v1/lembaga/')
        view = LembagaView.as_view(actions={"get": "list"})
        response = view(request)
        expected = Lembaga.objects.all()
        serialized = LembagaSerializer(expected, many=True, context={'request': request})
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_lembaga(self):
        factory = APIRequestFactory()
        json = {
            "tema": {
                "nama": "test_tema"
            },
            "institusi": {
                "nama": "test_institusi"
            },
            "nama": "hom",
            "jenis_pelayanan": "pim",
            "deskripsi_singkat": "pa",
            "praktikum_ke": 1,
            "beneficaries": "test_beneficaries",
            "alamat": "test_alamat",
            "last_praktikum": 2020
        }

        json_no_tema = {
            "tema": {
                "nama": "asal"
            },
            "institusi": {
                "nama": "test_institusi"
            },
            "nama": "hom",
            "jenis_pelayanan": "pim",
            "deskripsi_singkat": "pa",
            "praktikum_ke": 1,
            "beneficaries": "test_beneficaries",
            "alamat": "test_alamat",
            "last_praktikum": 2020
        }

        json_no_institusi = {
            "tema": {
                "nama": "test_tema"
            },
            "institusi": {
                "nama": "asal"
            },
            "nama": "hom",
            "jenis_pelayanan": "pim",
            "deskripsi_singkat": "pa",
            "praktikum_ke": 1,
            "beneficaries": "test_beneficaries",
            "alamat": "test_alamat",
            "last_praktikum": 2020
        }

        view = LembagaView.as_view(actions={"post": "create", "put": "update"})

        request = factory.post('/api/v1/lembaga/posts/', json, format='json')
        response = view(request)

        lembaga = Lembaga.objects.get(nama="hom")
        self.assertEqual(lembaga.jenis_pelayanan, "pim")

        request = factory.post('/api/v1/lembaga/posts/', json_no_tema, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 404)
        request = factory.post('/api/v1/lembaga/posts/', json_no_institusi, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 404)

        json_put = {
            "tema": {
                "nama": "test_tema"
            },
            "institusi": {
                "nama": "test_institusi"
            },
            "nama": "hom",
            "jenis_pelayanan": "akut",
            "deskripsi_singkat": "pa",
            "praktikum_ke": 1,
            "beneficaries": "test_beneficaries",
            "alamat": "test_alamat",
            "last_praktikum": 2020
        }

        id_lembaga = lembaga.id

        request = factory.put('/api/v1/lembaga/' + str(id_lembaga) + '/', json_put, format='json')
        response = view(request, pk=id_lembaga)

        lembaga = Lembaga.objects.get(nama="hom")
        self.assertEqual(lembaga.jenis_pelayanan, "akut")

    def test_get_lembaga_by_param_nama(self):
        """
        Test get lembaga with param nama API functionality
        """
        # Test API to get lembaga by name that contains substring _4
        param = {'nama': ['test_nama1']}
        factory = APIRequestFactory()
        request = factory.get('/api/v1/lembaga/', param)
        view = LembagaView.as_view(actions={"get": "list"})
        response = view(request)

        # Get All Elements in Object
        lembaga_objects = Lembaga.objects.all()
        # Generate Response
        expected = []
        for i in lembaga_objects:
            if param['nama'][0] in i.nama:
                expected.append(i)

        serialized = LembagaSerializer(expected, many=True, context={'request': request})
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lembaga_by_param_nama_not_exist(self):
        """
        Test get lembaga with param nama API functionality
        """
        # Test API to get lembaga by name that contains the given substring
        param = {'nama': ['test_nama1_1233241231231']}
        factory = APIRequestFactory()
        request = factory.get('/api/v1/lembaga/', param)
        view = LembagaView.as_view(actions={"get": "list"})
        response = view(request)

        # Get All Elements in Object
        lembaga_objects = Lembaga.objects.all()
        # Generate Response
        expected = []
        for i in lembaga_objects:
            if param['nama'][0] in i.nama:
                expected.append(i)

        serialized = LembagaSerializer(expected, many=True, context={'request': request})
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lembaga_by_param_tema(self):
        """
        Test get lembaga with param tema API functionality
        """
        param = {'tema': ['test_tema']}
        factory = APIRequestFactory()
        request = factory.get('/api/v1/lembaga/', param)
        view = LembagaView.as_view(actions={"get": "list"})
        response = view(request)
        expected = Lembaga.objects.all().filter(tema__nama__in=param['tema'])
        serialized = LembagaSerializer(expected, many=True, context={'request': request})
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lembaga_by_param_institusi(self):
        """
        Test get lembaga with param institusi API functionality
        """
        param = {'institusi': ['test_institusi']}
        factory = APIRequestFactory()
        request = factory.get('/api/v1/lembaga/', param)
        view = LembagaView.as_view(actions={"get": "list"})
        response = view(request)
        expected = Lembaga.objects.all().filter(institusi__nama__in=param['institusi'])
        serialized = LembagaSerializer(expected, many=True, context={'request': request})
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lembaga_by_all_param(self):
        """
        Test get lembaga with 2 param API functionality
        """
        param = {'tema': ['test_tema'], 'institusi': ['test_institusi']}
        factory = APIRequestFactory()
        request = factory.get('/api/v1/lembaga/', param)
        view = LembagaView.as_view(actions={"get": "list"})
        response = view(request)
        expected = Lembaga.objects.all().filter(institusi__nama__in=param['institusi']).filter(tema__nama__in=param['tema'])
        serialized = LembagaSerializer(expected, many=True, context={'request': request})
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lembaga_by_param_praktikum(self):
        """
        Test get lembaga with param praktikum API functionality
        """
        param = {'praktikum': ['Praktikum 1']}
        factory = APIRequestFactory()
        request = factory.get('/api/v1/lembaga/', param)
        view = LembagaView.as_view(actions={"get": "list"})
        response = view(request)
        expected = Lembaga.objects.all().filter(praktikum_ke__in=[1])
        serialized = LembagaSerializer(expected, many=True, context={'request': request})
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
