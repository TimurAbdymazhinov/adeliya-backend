import factory
from django.contrib.auth import get_user_model

from apps.account.models import City

User = get_user_model()


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    title = factory.Faker('city')


class UserFactory(factory.django.DjangoModelFactory):
    phone = factory.Sequence(lambda x: '+9967001112%02d' % x)
    is_registration_finish = False
    is_active = True
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    birth_date = factory.Faker('date')
    city = factory.SubFactory(CityFactory)

    class Meta:
        model = User
