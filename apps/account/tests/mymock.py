from rest_framework import status
from rest_framework.response import Response

from apps.account.tests import constants


class SuccessSmsNikitaResponse:
    def __init__(self):
        self.status_code = status.HTTP_200_OK
        self.text = constants.SMS_NIKITA_TEXT_ON_200_WITH_RESPONSE_STATUS_11


class SuccessSmsNikitaInvalidStatusResponse:
    def __init__(self):
        self.status_code = status.HTTP_200_OK
        self.text = constants.SMS_NIKITA_TEXT_ON_200_WITH_INVALID_RESPONSE_STATUS
