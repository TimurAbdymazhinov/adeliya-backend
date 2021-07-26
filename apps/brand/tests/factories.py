from random import choice

import factory

from apps.brand.models import (
    Brand, BrandImage,
    Filial, FilialImage, FilialPhone,
)


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    title = factory.Faker('company')
    logo = factory.django.ImageField(width=1024, height=768)
    description = factory.Faker('text')
    address = factory.Faker('address')
    link = factory.Faker('url')


class BrandImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BrandImage

    brand = None
    image = factory.django.ImageField(width=1024, height=768)


class FilialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Filial

    position = factory.Sequence(lambda x: '%d' % x)
    title = factory.Faker('name')
    address = factory.Faker('address')
    geolocation = "42.87962197359586,74.60025385022163"
    start_work = factory.Faker('time')
    end_work = factory.Faker('time')
    is_around_the_clock = factory.Sequence(lambda x: choice([True, False]))
    filial_1c_code = factory.Faker('random_number')


class FilialImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FilialImage

    filial = factory.SubFactory(FilialFactory)
    image = factory.django.ImageField(width=1024, height=768)
    is_main = factory.Sequence(lambda x: choice([True, False]))


class FilialPhoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FilialPhone
    filial = factory.SubFactory(FilialFactory)
    phone = factory.Faker('phone_number')
    is_phone = factory.Sequence(lambda x: choice([True, False]))
    is_whatsapp = factory.Sequence(lambda x: choice([True, False]))
