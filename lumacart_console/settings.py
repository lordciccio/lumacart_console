"""
Django settings for lumacart_console project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9!s+vz&sab=xyb6v+&hcxffv!jj36t(fjojhvw)&3nh7#e0p1%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lumacart_console.catalogue',
    'lumacart_console.orders'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'lumacart_console.urls'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'it-it'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler"]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
             os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':  os.path.join(BASE_DIR, 'console.log'),
            'maxBytes': 1024*1024*10, # 10 MB
            'backupCount': 5,
            'formatter':'verbose'
        },
    },
    'loggers': {
        'project': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG'
        }
    },
}

from lumacart_console import prod_params

HOST = prod_params.HOST
EMAIL_SENDER = prod_params.EMAIL_SENDER
EMAIL_SUBJECT_PREFIX = "[Lumacart Console] "
EMAIL_HOST = prod_params.EMAIL_HOST
EMAIL_HOST_USER = prod_params.EMAIL_HOST_USER
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = prod_params.EMAIL_HOST_PASSWORD
ADMIN_EMAIL = prod_params.ADMIN_EMAIL

C2O_API_KEY = prod_params.C2O_API_KEY

ETSY_SHOP_ID = prod_params.ETSY_SHOP_ID
ETSY_RESOURCE_OWNER_KEY = prod_params.ETSY_RESOURCE_OWNER_KEY
ETSY_RESOURCE_OWNER_SECRET = prod_params.ETSY_RESOURCE_OWNER_SECRET
ETSY_CLIENT_KEY = prod_params.ETSY_CLIENT_KEY
ETSY_CLIENT_SECRET = prod_params.ETSY_CLIENT_SECRET

WOO_SITE_URL = "http://www.lumacart.com"
WOO_CONSUMER_KEY = "ck_c3d5e7bee827b6e6b2b8a09aacde60e538a7eda2"
WOO_CONSUMER_SECRET = "cs_0097da6cf98fba220e2d16f17e5735bc7c27e38b"
