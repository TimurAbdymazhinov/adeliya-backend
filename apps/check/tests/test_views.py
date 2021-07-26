from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.account.tests.factories import UserFactory


class QRCodeAPIViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('v1:qr_code')
        user = UserFactory()
        cls.token = Token.objects.create(user=user)

    def setUp(self) -> None:
        self.client = APIClient()

    def test_success_get_qr_code_on_200(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_fail_get_qr_code_on_401(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
