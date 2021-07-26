import environ
from rest_framework import permissions

env = environ.Env()


SECRET_KEY = env.str('DJANGO_SECRET_KEY', default='not secret)')

DEBUG = env.bool('DJANGO_DEBUG', default=True)

DATABASES = {
    'default': env.db(
        'DATABASE_URL', default='sqlite:///db.sqlite'
    )
}

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])

if DEBUG:
    API_PERMISSION = permissions.AllowAny
else:
    API_PERMISSION = permissions.IsAuthenticated

INTERNAL_IPS = [
    '127.0.0.1',
]
