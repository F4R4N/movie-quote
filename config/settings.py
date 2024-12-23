from pathlib import Path
from datetime import timedelta
import os


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = str(os.environ.get("CONFIG_SECRET_KEY"))

DEBUG = bool(int(os.environ.get("CONFIG_DEBUG", 0)))

ALLOWED_HOSTS = os.environ.get("CONFIG_ALLOWED_HOSTS", []).split(", ")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'statistic.apps.StatisticConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'corsheaders',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # path to load email templates
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

WSGI_APPLICATION = 'config.wsgi.application'
# database configs
DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": int(os.environ.get("DB_PORT")),
    }
}
PASSWORD_VALIDATOR = 'django.contrib.auth.password_validation.'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': f'{PASSWORD_VALIDATOR}UserAttributeSimilarityValidator',
    },
    {
        'NAME': f'{PASSWORD_VALIDATOR}MinimumLengthValidator',
    },
    {
        'NAME': f'{PASSWORD_VALIDATOR}CommonPasswordValidator',
    },
    {
        'NAME': f'{PASSWORD_VALIDATOR}NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True
# disabled to solve bugs with statistic visit object creation and complicities
# with different timezones
USE_TZ = False

# STATIC_URL = '/static/'
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
# simplejwt configs
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# swagger configs
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# ipstack api access key
IPSTACK_ACCESS_KEY = os.environ.get("IPSTACK_ACCESS_KEY")
# email configs
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("CONFIG_EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("CONFIG_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("CONFIG_EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_PORT = 587

CORS_ALLOW_ALL_ORIGINS = True
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 259200
    # redirect HTTP request to HTTPS
    SECURE_SSL_REDIRECT = bool(
        int(os.environ.get("CONFIG_SECURE_SSL_REDIRECT", 1)))

    SECURE_PROXY_SSL_HEADER = tuple(
        os.environ.get("CONFIG_SECURE_PROXY_SSL_HEADER").split(", ")
    )
