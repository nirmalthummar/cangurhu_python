from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'sslserver',
    'corsheaders',
    'django_extensions',
]

# External Apps
EXTERNAL_APPS = [
    'rest_framework',
    'django_filters',
    'drf_yasg',
    'django_otp',
    'django_celery_beat',
    'django_celery_results',
    'django_summernote',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

]

CUSTOM_APPS = [
    'apps.accounts',
    'apps.customer',
    'apps.cook',
    'apps.courier',
    'apps.cart',
    'apps.snippets',
    'apps.dashboard',
    'apps.address',
    'apps.contents',
    'apps.order',
    'apps.rating',
    'apps.config',
    'apps.notification',
]

INSTALLED_APPS += EXTERNAL_APPS + CUSTOM_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_http_referrer_policy.middleware.ReferrerPolicyMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
    'COERCE_DECIMAL_TO_STRING': False,

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.accounts.backends.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'core.renderers.CustomRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 20,
    'page_size_query_param': 'page_size',
}

AUTH_USER_MODEL = 'accounts.User'

ROOT_URLCONF = 'cangurhu.urls'

TEMPLATE_PATH = BASE_DIR / 'templates'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_PATH, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'url_tag': 'templatetags.template_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'cangurhu.wsgi.application'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend', 'allauth.account.auth_backends.AuthenticationBackend']



# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}


SOCIALACCOUNT_AUTHENTICATION_METHOD = 'oauth2'

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id': 'your-client-id',
#             'secret': 'your-client-secret',
#             'key': ''
#         }
#     }
# }


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

SITE_ID = 2


# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = Path(BASE_DIR).resolve().parent / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = Path(BASE_DIR).resolve().parent / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Configuration
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
EMAIL_PORT = config('EMAIL_PORT', cast=int)

SENDER_EMAIL = config('SENDER_EMAIL')
SENDER_NAME = config('SENDER_NAME')
REPLY_EMAIL = config('REPLY_EMAIL')

SITE_URL = config('SITE_URL')
SITE_NAME = config('SITE_NAME')

FIREBASE_SERVER_KEY = config('FIREBASE_SERVER_KEY')

TOTP_TOKEN_VALIDITY = 600
TOTP_DIGITS = 4

# CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
# CELERY_RESULT_BACKEND = "django-db"

#######################
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Dhaka'
#######################

LOGIN_URL = '/Dashboard/Login/'

SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "cangurhu.swagger.CustomAutoSchema",
    "SHOW_REQUEST_HEADERS": True,
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
}

# CRONJOBS = [
# ('*/1 * * * *', 'cron.index')
# ]
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_TRACK_STARTED = True
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/'

# Cors Origin
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOWED_ORIGINS = [
#     'https://quytech.in',
#     'http://13.127.138.63',
#     'http://localhost'
# ]


CORS_ALLOW_HEADERS = ['*']
REFERRER_POLICY = 'unsafe-url'
# SMS GATEWAY CONFIGURATION

ACCOUNT_SID = config('ACCOUNT_SID')
AUTH_TOKEN = config('AUTH_TOKEN')
PHONE_NUMBER = config('PHONE_NUMBER')
