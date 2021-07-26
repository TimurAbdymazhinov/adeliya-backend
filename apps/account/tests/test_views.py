import json
from unittest import mock

from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.account.service import UserAuthService, ChangeOldPhoneService
from apps.account.tests.factories import UserFactory, CityFactory
from apps.account.tests.mymock import (
    SuccessSmsNikitaResponse, SuccessSmsNikitaInvalidStatusResponse,
    failure_compare_confirmation_time, SuccessChangePhone,
)
from apps.account.utils import generate_photo_file
from core.constants import MALE


class AuthorizedTestMixin:
    def test_unauthorized_on_401(self):
        client = APIClient()
        response = client.get(self.url)
        expected_data = {'detail': 'Учетные данные не были предоставлены.'}
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(expected_data, json.loads(response.content))

    def test_get_invalid_token_on_401(self):
        user = UserFactory()
        token = Token.objects.create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key + 'a')
        response = client.get(self.url)
        expected_data = {'detail': 'Недопустимый токен.'}
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(expected_data, json.loads(response.content))


class AuthAPIViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        UserFactory(phone='+996553000117', is_registration_finish=True)
        UserFactory(
            phone='+996553000118', is_active=False, is_registration_finish=True,
        )
        cls.client = Client()
        cls.auth_url = reverse('v1:auth')

    @mock.patch('requests.post', return_value=SuccessSmsNikitaResponse())
    def test_success_status_on_201(self, mocked):
        phone_data = {'phone': '+996999111222'}
        response = self.client.post(self.auth_url, data=phone_data)
        expected_data = {'message': 'User создан! Сообщение отправлено'}
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected_data, response.data)

    @mock.patch('requests.post', return_value=SuccessSmsNikitaResponse())
    def test_success_status_on_200(self, mocked):
        phone_data = {'phone': '+996553000117'}
        response = self.client.post(self.auth_url, data=phone_data)
        expected_data = {'message': 'Сообщение отправлено'}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_is_not_active_user_status_on_400(self):
        phone_data = {'phone': '+996553000118'}
        response = self.client.post(self.auth_url, data=phone_data)
        expected_data = {'phone': ['Этот номер не активен.']}
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(expected_data, json.loads(response.content))

    @mock.patch('requests.post', return_value=SuccessSmsNikitaInvalidStatusResponse())
    def test_sms_nikita_with_invalid_status_on_400(self, mocked):
        phone_data = {'phone': '+996999111222'}
        response = self.client.post(self.auth_url, data=phone_data)
        expected_data = {'message': 'Не удалось отправить сообщение. Попробуйте позже.'}
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(expected_data, response.data)

    @mock.patch.object(UserAuthService, 'compare_confirmation_time', return_value=failure_compare_confirmation_time())
    def test_failure_too_many_requests_on_429(self, mocked):
        phone_data = {'phone': '+996999111222'}
        response = self.client.post(self.auth_url, data=phone_data)
        expected_data = {'message': 'Вы слишком часто отправляете сообщение.'}
        self.assertEqual(status.HTTP_429_TOO_MANY_REQUESTS, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_failure_phone_validate_on_400(self):
        phone_data = {'phone': '+996999111222a'}
        response = self.client.post(self.auth_url, data=phone_data)
        expected_data = {'phone': ['phone is not valid!']}
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(expected_data, json.loads(response.content))


class LoginConfirmAPIViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        UserFactory(phone='+996999111222', is_active=True, confirmation_code='123456')
        UserFactory(phone='+996701626702', is_active=False, confirmation_code='123456')
        UserFactory(phone='+996701626700', confirmation_code='123456',)
        cls.url = reverse('v1:login-confirm')

    def test_success_login_confirmation_with_profile_completed_on_200(self):
        data = {'phone': '+996701626700', 'confirmation_code': '123456'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(True, response.data.get('is_profile_completed'))

    def test_success_login_confirmation_without_profile_completed_on_200(self):
        data = {'phone': '+996999111222', 'confirmation_code': '123456'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_failure_not_valid_confirmation_code_on_403(self):
        data = {'phone': '+996999111222', 'confirmation_code': '123455'}
        expected_data = {'message': 'Неверный код'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_is_not_active_user_on_400(self):
        data = {'phone': '+996701626702', 'confirmation_code': '123456'}
        response = self.client.post(self.url, data=data)
        expected_data = {'phone': ['Этот номер не активен.']}
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(expected_data, json.loads(response.content))

    def test_not_exist_user_on_404(self):
        data = {'phone': '+996701626705', 'confirmation_code': '123456'}
        response = self.client.post(self.url, data=data)
        expected_data = {'detail': 'user not found'}
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(expected_data, json.loads(response.content))

    def test_failure_phone_validate_on_400(self):
        phone_data = {'phone': '+996999111222a', 'confirmation_code': '123456'}
        response = self.client.post(self.url, data=phone_data)
        expected_data = {'phone': ['phone is not valid!']}
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(expected_data, json.loads(response.content))


class CityListAPIViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CityFactory()
        CityFactory()
        cls.url = reverse('v1:cities')
        cls.client = Client()

    def test_city_list_api(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class UserRetrieveUpdateAPIViewTest(AuthorizedTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('v1:retrieve-update')
        user = UserFactory()
        cls.token = Token.objects.create(user=user)
        cls.city = user.city

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_success_on_200(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put_bad_request_on_400(self):
        response = self.client.put(self.url, {})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put_success_on_200(self):
        data = {
            'first_name': 'Aman',
            'last_name': 'Kalmanbetov',
            'gender': MALE,
            'birth_date': '1975-05-09',
            'city': self.city.id,
        }
        response = self.client.put(self.url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Aman', response.data.get('first_name'))
        self.assertEqual('Kalmanbetov', response.data.get('last_name'))

    def test_patch_success_on_200(self):
        data = {'first_name': 'Amanbek'}
        response = self.client.patch(self.url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Amanbek', response.data.get('first_name'))


class UserAvatarRetrieveUpdateAPIViewTest(AuthorizedTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('v1:avatar')
        user = UserFactory()
        cls.token = Token.objects.create(user=user)

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_success_update_avatar_on_200(self):
        data = {'avatar': generate_photo_file()}
        response = self.client.patch(self.url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class SendSmsToOldPhoneAPIViewTest(AuthorizedTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('v1:send_sms_to_old_phone')
        cls.user = UserFactory()
        cls.token = Token.objects.create(user=cls.user)

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @mock.patch.object(UserAuthService, 'compare_confirmation_time', return_value=failure_compare_confirmation_time())
    def test_failure_too_many_requests_on_429(self, mocked):
        response = self.client.get(self.url)
        expected_data = {'message': 'Вы слишком часто отправляете сообщение.'}
        self.assertEqual(status.HTTP_429_TOO_MANY_REQUESTS, response.status_code)
        self.assertEqual(expected_data, response.data)

    @mock.patch('requests.post', return_value=SuccessSmsNikitaResponse())
    def test_success_status_on_200(self, mocked):
        response = self.client.get(self.url)
        expected_data = {'message': 'Сообщение отправлено'}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    @mock.patch('requests.post', return_value=SuccessSmsNikitaInvalidStatusResponse())
    def test_sms_nikita_with_invalid_status_on_400(self, mocked):
        response = self.client.get(self.url)
        expected_data = {'message': 'Не удалось отправить сообщение. Попробуйте позже.'}
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(expected_data, response.data)


class OldPhoneConfirmAPIViewTest(AuthorizedTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('v1:old_phone_confirm')

    def setUp(self) -> None:
        self.user = UserFactory(confirmation_code='123456')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_failure_not_valid_confirmation_code_on_403(self):
        data = {'confirmation_code': '123455'}
        expected_data = {'message': 'Неверный код'}
        response = self.client.post(self.url, data=data)
        self.user.refresh_from_db()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(expected_data, response.data)
        self.assertEqual(False, self.user.is_old_phone_confirmed)

    def test_success_confirmation_on_200(self):
        data = {'confirmation_code': '123456'}
        response = self.client.post(self.url, data=data)
        expected_data = {"message": "Old phone is confirmed"}
        self.user.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)
        self.assertEqual(True, self.user.is_old_phone_confirmed)


class SendSmsToNewPhoneAPIVewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory(phone='+996553000117', is_registration_finish=True)
        cls.url = reverse('v1:change_old_phone')
        cls.token = Token.objects.create(user=cls.user)

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @mock.patch('requests.post', return_value=SuccessSmsNikitaResponse())
    def test_success_status_on_200(self, mocked):
        phone_data = {'phone': '+996553000119'}
        response = self.client.post(self.url, data=phone_data)
        expected_data = {'message': 'Сообщение отправлено'}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    @mock.patch('requests.post',
                return_value=SuccessSmsNikitaInvalidStatusResponse())
    def test_sms_nikita_with_invalid_status_on_400(self, mocked):
        phone_data = {'phone': '+996999111222'}
        response = self.client.post(self.url, data=phone_data)
        expected_data = {
            'message': 'Не удалось отправить сообщение. Попробуйте позже.'}
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_checking_for_uniqueness_with_status_on_406(self):
        phone_data = {'phone': '+996553000117'}
        response = self.client.post(self.url, data=phone_data)
        expected_data = {'message': 'Такой номер телефона уже существует'}
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_failure_too_many_requests_on_429(self):
        phone_data = {'phone': '+996999111222'}
        response = self.client.post(self.url, phone_data)
        response = self.client.post(self.url, phone_data)
        expected_data = {'message': 'Вы слишком часто отправляете сообщение.'}
        self.assertEqual(status.HTTP_429_TOO_MANY_REQUESTS,
                         response.status_code)
        self.assertEqual(expected_data, response.data)


class NewPhoneConfirmAPIViewTest(AuthorizedTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('v1:new_phone_confirm')
        cls.user = UserFactory(confirmation_code='123456')
        cls.token = Token.objects.create(user=cls.user)

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_failure_not_valid_confirmation_code_on_403(self):
        data = {'confirmation_code': '123455'}
        expected_data = {'message': 'Неверный код'}
        response = self.client.post(self.url, data=data)
        self.user.refresh_from_db()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(expected_data, response.data)
        self.assertEqual(False, self.user.is_old_phone_confirmed)

    """ Don't forget to added test for ChangePhoneSerializer """
