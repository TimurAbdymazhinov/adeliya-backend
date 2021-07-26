from random import choice
import datetime

import factory

from apps.setting.models import AppVersion, Setting


class AppVersionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AppVersion

    android_version = factory.Sequence(lambda n: '1.%d' % choice([1, 2, 3]))
    android_force_update = factory.Sequence(lambda x: choice([True, False]))
    ios_version = factory.Sequence(lambda n: '1.%d' % choice([1, 2, 3]))
    ios_force_update = factory.Sequence(lambda x: choice([True, False]))


class SettingFactory(factory.django.DjangoModelFactory):
    qr_code_expiration_date = factory.LazyFunction(datetime.timedelta)
    is_service_active = False

    class Meta:
        model = Setting
