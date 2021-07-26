from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from apps.setting.tests.factories import SettingFactory


class SettingMiddlewareTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_url = reverse('admin:index')
        cls.default_url = reverse('v1:brand_list')
        SettingFactory()

    def setUp(self) -> None:
        self.client = APIClient()

    def test_success_get_admin_page_302(self):
        response = self.client.get(self.admin_url)

        self.assertEqual(status.HTTP_302_FOUND, response.status_code)

    def test_fail_get_non_admin_page_503(self):
        response = self.client.get(self.default_url)
        self.assertEqual(
            status.HTTP_503_SERVICE_UNAVAILABLE, response.status_code
        )
