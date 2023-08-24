import os
from datetime import timedelta

import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(
    DEBUG=(bool, True),
    HOMME_SECRET_KEY=(str, 'secret'),
    HOMME_DB_ENGINE=(str, 'django.db.backends.postgresql'),
    HOMME_DB_NAME=(str, 'homme'),
    HOMME_DB_USER=(str, 'root'),
    HOMME_DB_PORT=(int, 3306),
    HOMME_DB_HOST=(str, 'homme-db'),
    HOMME_DB_PASSWORD=(str, 'homme'),
    BASE_URL_FE=(str, 'https://stage.crymzee.com'),
    AWS_DEFAULT_REGION=(str, 'eu-central-1'),
    ELASTIC_URL=(str, 'elastic:9200'),
    DEBUG_LEVEL=(str, 'INFO'),
    DEFAULT_FROM_EMAIL=(str, 'sadevtest44@gmail.com'),
)
environ.Env.read_env(f"{BASE_DIR}/.env")

# GDAL_LIBRARY_PATH = env.str("GDAL_LIBRARY_PATH")
# GEOS_LIBRARY_PATH = env.str("GEOS_LIBRARY_PATH")

SECRET_KEY = env('HOMME_SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False

# SMTP email configurations
EMAIL_USE_TLS = env.bool('HOMME_EMAIL_USE_TLS', default=True)
EMAIL_HOST = env.str('HOMME_EMAIL_HOST')
EMAIL_PORT = env.int('HOMME_EMAIL_PORT')
EMAIL_HOST_USER = env.str('HOMME_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('HOMME_EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# Application definition
DJANGO_APPS = [
    'material',
    'material.admin',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.gis',
]

THIRD_INSTALLED_APP = [
    'drf_yasg',
    'corsheaders',
    'django_cleanup.apps.CleanupConfig',
    'django_rest_passwordreset',
    'rest_framework',
    'geoip2',
    'django_elasticsearch_dsl',
    "fcm_django",
]

APPS = [
    'api.core',
    'api.jwtauth',
    'api.users',
    'api.categories',
    'api.product_types',
    'api.vendors',
    'api.products',
    'api.support',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_INSTALLED_APP + APPS
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

ORGS_SLUGFIELD = 'django_extensions.db.fields.AutoSlugField'
X_FRAME_OPTIONS = 'SAMEORIGIN'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.core.middlewares.ApiMiddleware',
    'api.core.middlewares.PrintSQlMiddleware'
]

AUTH_USER_MODEL = 'users.User'
APPEND_SLASH = False

# Cors

CORS_ORIGIN_WHITELIST = []

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'token',
    'cache-control',
    'Device-Type'
)
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

STATIC_URL = env.str("HOMME_STATIC_URL", "/staticfiles/")
MEDIA_URL = env.str("HOMME_MEDIA_URL", "/mediafiles/")
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

DEFAULT_PROFILE_IMAGE = "default-profile.png"
DEFAULT_PROFILE_IMAGE_URL = os.path.join(MEDIA_URL, DEFAULT_PROFILE_IMAGE)


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIRS[0]],
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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        'ENGINE': env('HOMME_DB_ENGINE'),
        'NAME': env('HOMME_DB_NAME'),
        'USER': env('HOMME_DB_USER'),
        'PASSWORD': env('HOMME_DB_PASSWORD'),
        'HOST': env('HOMME_DB_HOST'),
        'PORT': env('HOMME_DB_PORT'),
        'CONN_MAX_AGE': None
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['api.core.backends.CustomJWTAuthentication'],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated",
                                   "api.core.permissions.RoleEqualToDeviceHeader"],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser'
    ],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'EXCEPTION_HANDLER': 'api.core.utils.custom_exception_handler',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'config.pagination.CustomPagination',
    'PAGE_SIZE': 5,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        },
        'Device-type': {
            'type': 'apiKey',
            'name': 'Device-Type',
            'in': 'header'
        },
        'REFETCH_SCHEMA_WITH_AUTH': True
    },
    'DEFAULT_AUTO_SCHEMA_CLASS': 'api.core.mixin.CustomAutoSchema'
}

LOGIN_URL = 'token_obtain_pair'
LOGIN_REDIRECT_URL = 'api/swagger'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=env.int('HOMME_ACCESS_TOKEN_LIFETIME_SEC', default=timedelta(hours=10))),
    'REFRESH_TOKEN_LIFETIME': timedelta(seconds=env.int('HOMME_REFRESH_TOKEN_LIFETIME_SEC', default=timedelta(days=10))),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=160),
}

# stripe configs
STRIPE_SECRET_KEY = env.str('HOMME_STRIPE_KEY')
STRIPE_PUBLIC_KEY = env.str('HOMME_STRIPE_PUBLIC_KEY')
STRIPE_CURRENCY = env.str('HOMME_STRIPE_CURRENCY')

TIME_ZONE = env.str("HOMME_TIME_ZONE", 'UTC')
NUMBER_OF_CHARACTERS = 160
USE_I18N = True
USE_L10N = True
USE_TZ = env.bool("HOMME_USE_TZ", False)

# OTP configuration
OTP_TIMEOUT_SECONDS = env.int('HOMME_OTP_TIMEOUT_SECONDS', default=30000)
OTP_VERIFICATION_TIMEOUT_SECONDS = env.int('HOMME_OTP_VERIFICATION_TIMEOUT_SECONDS', default=30000)

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Debug
DEBUG_LEVEL = env('DEBUG_LEVEL')

# Elasticsearch

ELASTICSEARCH_DSL = {'default': {'hosts': env("ELASTIC_URL")}}
BASE_URL_FE = env('BASE_URL_FE')



