import os
from .base import *

SECRET_KEY=os.environ['SECRET_KEY_RAZ']

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

#TEST_DATABASE_CHARSET=UTF8
#CHARSET=UTF8 # supported for PG and MySQL only
