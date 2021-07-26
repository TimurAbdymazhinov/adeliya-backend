from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.info.models import (
    Banner,
    ProgramCondition,
    Contact, PromotionAndNews,
)
from .factories import (
    BannerFactory,
    ProgramConditionFactory,
    ContactFactory,
    PromotionAndNewsImageFactory,
    PromotionAndNewsFactory,
)


class BannerAndPromotionTest(APITestCase):

    def setUp(self) -> None:
        self.banner = BannerFactory()
        self.url = reverse('v1:banner-promotions')

    def test_get_banner(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.banner.title, response.data['banner']['title'])

    def test_get_banner_on_empty_db_table(self) -> None:
        Banner.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['banner'], None)
        self.assertEqual(response.data['promotion'], [])


class BannerTest(APITestCase):

    def setUp(self) -> None:
        self.banner = BannerFactory()
        self.url = reverse('v1:banner-detail')

    def test_get_banner(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data['title'], self.banner.title)
        self.assertIn(
            response.data['description'], self.banner.description
        )

    def test_get_banner_on_empty_db_table(self) -> None:
        Banner.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data['title'], '')
        self.assertIn(
            response.data['description'], ''
        )


class ProgramConditionTest(APITestCase):

    def setUp(self) -> None:
        self.program_condition = ProgramConditionFactory()
        self.url = reverse('v1:program_condition')

    def test_get_program_condition(self) -> None:
        response = self.client.get(self.url)
        expected_data = {
            'id': 1,
            'title': self.program_condition.title,
            'description': self.program_condition.description
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_program_condition_on_empty_db_table(self) -> None:
        ProgramCondition.objects.all().delete()
        response = self.client.get(self.url)
        expected_data = {
            'title': '',
            'description': '',
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class TestContactListAPIView(APITestCase):

    def setUp(self) -> None:
        self.insta = ContactFactory()
        self.vk = ContactFactory()
        self.url = reverse('v1:contacts')

    def test_get_contacts(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.insta.title, response.data[0]['title'])
        self.assertIn(self.vk.title, response.data[1]['title'])

    def test_get_contacts_on_empty_db_table(self) -> None:
        Contact.objects.all().delete()
        response = self.client.get(self.url)
        expected_data = []
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class PromotionAndNewsListTest(APITestCase):
    def setUp(self) -> None:
        self.article = PromotionAndNewsImageFactory()
        self.url = reverse('v1:promotions-news')

    def test_get_promotion_and_news(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.article.information.title,
            response.data['results'][0]['title']
        )

    def test_get_promotions_news_list_on_empty_db_table(self):
        PromotionAndNews.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])


class PromotionAndNewsDetail(APITestCase):
    def setUp(self) -> None:
        self.article = PromotionAndNewsFactory()

    def test_get_promotions_and_news_detail(self):
        url = reverse('v1:promotions-news-detail', kwargs={'pk': self.article.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.article.title)

    def test_get_promotions_and_news_detail_on_empty_db_table(self):
        url = reverse('v1:promotions-news-detail', kwargs={'pk': 260})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Страница не найдена.')
