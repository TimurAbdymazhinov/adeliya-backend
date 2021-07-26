import os
import logging

import environ

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))

env = environ.Env()

INSTALLED_APPS = [
    'huey.contrib.djhuey',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework.authtoken',
    'rest_framework',
    'solo',
    'ckeditor',
    'django_2gis_maps',
    'fcm_django',
    'drf_yasg',
    'django_filters',
    'adminsortable2',

    'apps.account',
    'apps.brand',
    'apps.check',
    'apps.info',
    'apps.setting',
    'apps.notifications',
]

FCM_DJANGO_SETTINGS = {
    # Your firebase API KEY
    "FCM_SERVER_KEY": env.str('FCM_SERVER_KEY'),
    # true if you want to have only one active device per registered user at a time
    # default: False
    "ONE_DEVICE_PER_USER": False,
    # devices to which notifications cannot be sent,
    # are deleted upon receiving error response from FCM
    # default: False
    "DELETE_INACTIVE_DEVICES": True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.setting.middleware.ApplicationStatusMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

AUTH_USER_MODEL = 'account.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

JET_SIDE_MENU_COMPACT = True

# ckeditor
CKEDITOR_UPLOAD_PATH = "uploads/"

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

NIKITA_LOGIN = env.str('NIKITA_LOGIN')
NIKITA_PASSWORD = env.str('NIKITA_PASSWORD')
NIKITA_SENDER = env.str('NIKITA_SENDER')
NIKITA_TEST = env.int('NIKITA_TEST', default=1)

BASE_1C_SERVER_DOMAIN = env.str(
    'BASE_1C_SERVER_DOMAIN', default='http://185.29.184.147:12344'
)

LINKS_1C = {
    'SYNC_USER_URL': BASE_1C_SERVER_DOMAIN + '/sendUser',
    'GET_USER_WALLET_DATA_URL':
        BASE_1C_SERVER_DOMAIN + '/userPoint/',
    'CHANGE_USER_NUMBER': BASE_1C_SERVER_DOMAIN + '/change_number'
}

USER_1C = {
    'username': env.str('USER_1C_USERNAME'),
    'password': env.str('USER_1C_PASSWORD')
}


LOGGING = {
    "version": 1,
    "formatters": {"simple": {"format": "{levelname} {message}", "style": "{"}},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        }
    },
    "loggers": {
        "django": {"handlers": ["console"], "propagate": True},
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

HUEY = {
    'huey_class': 'huey.RedisHuey',  # Huey implementation to use.
    'immediate': False,
    'connection': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'connection_pool': None,  # Definitely you should use pooling!
        # ... tons of other options, see redis-py for details.

        # huey-specific connection parameters.
        'read_timeout': 1,  # If not polling (blocking pop), use timeout.
        'url': None,  # Allow Redis config via a DSN.
    },

    'consumer': {
        'workers': 5,
        'worker_type': 'thread',
        'initial_delay': 0.1,  # Smallest polling interval, same as -d.
        'backoff': 1.15,  # Exponential backoff using this rate, -b.
        'max_delay': 10.0,  # Max possible polling interval, -m.
        'scheduler_interval': 1,  # Check schedule every second, -s.
        'periodic': True,  # Enable crontab feature.
        'check_worker_health': True,  # Enable worker health checks.
        'health_check_interval': 1,  # Check worker health every second.
    },
}

try:
    from .local import *
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
except ImportError:
    try:
        from .prod import *
    except ImportError:
        logging.error('core.settings.prod.py file not found !')
