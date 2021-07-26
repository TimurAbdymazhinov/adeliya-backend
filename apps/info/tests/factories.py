from random import choice

import factory

from apps.info.models import (
    Banner, ProgramCondition,
    Contact, PromotionAndNews,
    PromotionAndNewsImage, ContactIcon,
)
from core.constants import PROMOTION, NEWS


class ContactIconFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactIcon

    title = factory.Faker('name')
    image = factory.django.ImageField(width=1024, height=768)


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    title = factory.Faker('name')
    link = factory.Faker('url')
    icon_image = factory.SubFactory(ContactIconFactory)


class BannerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Banner

    title = factory.Faker('name')
    image = factory.django.ImageField(width=1024, height=768)
    description = factory.Faker('text')


class ProgramConditionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProgramCondition

    title = factory.Faker('name')
    description = factory.Faker('text')


class PromotionAndNewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PromotionAndNews

    information_type = factory.Sequence(lambda x: choice([PROMOTION, NEWS]))
    created_at = factory.Faker('date_time')
    title = factory.Faker('city')
    description = factory.Faker('text')
    is_active = True


class PromotionAndNewsImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PromotionAndNewsImage

    image = factory.django.ImageField(width=1024, height=768)
    is_main = factory.Sequence(lambda x: choice([True, False]))
    information = factory.SubFactory(PromotionAndNewsFactory)
