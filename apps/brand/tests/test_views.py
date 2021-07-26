from collections import OrderedDict

from django.urls import reverse

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from apps.brand.models import Brand


class TestBrandListAPIView(APITestCase):
    def setUp(self) -> None:
        Brand.objects.create(
            id=1,
            title="brand1", logo='brand_logo1.img', description='brand1 description',
            address='brand1 address', link='http://localhost:8000'
        )
        Brand.objects.create(
            id=2,
            title="brand2", logo='brand_logo2.img', description='brand2 description',
            address='brand2 address', link='http://localhost:8000'
        )
        self.url = reverse('v1:brand_list')

    def test_get_brand_list(self):
        response = self.client.get(self.url)
        expected_data = {
            'count': 2, 'next': None, 'previous': None,
            'results': [
                OrderedDict([
                    ('id', 1), ('logo', 'http://testserver/media/brand_logo1.img')
                ]),
                OrderedDict([
                    ('id', 2), ('logo', 'http://testserver/media/brand_logo2.img')
                ])]
        }
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_data_if_model_is_empty(self):
        Brand.objects.all().delete()
        response = self.client.get(self.url)
        expected_data = {'count': 0, 'next': None, 'previous': None, 'results': []}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class TestBrandRetrieveAPIView(APITestCase):

    def setUp(self) -> None:
        Brand.objects.create(
            id=1,
            title="brand1", logo='brand_logo1.img', description='brand1 description',
            address='brand1 address', link='http://localhost:8000'
        )
        Brand.objects.create(
            id=2,
            title="brand2", logo='brand_logo2.img', description='brand2 description',
            address='brand2 address', link='http://localhost:8000'
        )

    def test_get_brand_detail(self):
        url = reverse('v1:brand_detail', kwargs={'id': 1})
        response = self.client.get(url)
        expected_data = {
            'title': 'brand1', 'description': 'brand1 description',
            'address': 'brand1 address', 'link': 'http://localhost:8000',
            'images': [],
        }
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_brand_data_if_model_is_empty(self):
        Brand.objects.all().delete()
        url = reverse('v1:brand_detail', kwargs={'id': 100})
        response = self.client.get(url)
        expected_data = {
            'detail': ErrorDetail(string='Страница не найдена.', code='not_found'),
        }
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected_data)

    def test_get_brand_data_if_incorrect_key(self):
        url = reverse('v1:brand_detail', kwargs={'id': 10})
        response = self.client.get(url)
        expected_data = {
            'detail': ErrorDetail(string='Страница не найдена.', code='not_found'),
        }
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected_data)
