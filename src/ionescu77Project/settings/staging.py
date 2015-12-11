import os
from .base import *

SECRET_KEY=os.environ['SECRET_KEY_RAZ']


# Setup Database
from .database_staging import DATABASES
DATABASES = DATABASES

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



INSTALLED_APPS += ('django_jenkins',)
JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
)
PROJECT_APPS = ['blogengine']
