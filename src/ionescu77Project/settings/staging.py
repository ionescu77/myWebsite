import os
from .base import *

SECRET_KEY=os.environ['SECRET_KEY_RAZ']
DB_USER_IONESCU77=os.environ['DB_USER_IONESCU77']
DB_PASS_IONESCU77=os.environ['DB_PASS_IONESCU77']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ionescu77db',
        'USER': DB_USER_IONESCU77,
        'PASSWORD': DB_PASS_IONESCU77,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['ionescu77.avproiect.com']

INSTALLED_APPS += (
    'landing',
    'blogengine',
    'django.contrib.sites',
    'django.contrib.flatpages',
)

SITE_ID = 1

#TEST_DATABASE_CHARSET=UTF8
#CHARSET=UTF8 # supported for PG and MySQL only

STATIC_ROOT = "/var/www/myProjects/ionescu77/static/"
MEDIA_ROOT = "/var/www/myProjects/ionescu77/media/"
