import environ
from rest_framework import permissions

env = environ.Env()


SECRET_KEY = env.str('DJANGO_SECRET_KEY')

DEBUG = env.bool('DJANGO_DEBUG')

DATABASES = {'default': env.db('DATABASE_URL')}

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

if DEBUG:
    API_PERMISSION = permissions.AllowAny
else:
    API_PERMISSION = permissions.IsAuthenticated
