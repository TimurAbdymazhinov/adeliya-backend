from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.setting.models import AppVersion
from .factories import AppVersionFactory


class AppVersionTest(APITestCase):

    def setUp(self) -> None:
        self.app_version = AppVersionFactory()
        self.url = reverse('v1:app-version')

    def test_get_app_version(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.app_version.android_version, response.data['android_version'])

    def test_get_app_version_on_empty_db_table(self):
        AppVersion.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('', response.data['android_version'])
