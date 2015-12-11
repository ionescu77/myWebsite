# Database on staging:
# Data is passed from ENV Variables or from activate

DB_NAME_IONESCU77=os.environ['DB_NAME_IONESCU77']
DB_USER_IONESCU77=os.environ['DB_USER_IONESCU77']
DB_PASS_IONESCU77=os.environ['DB_PASS_IONESCU77']
DB_PORT_IONESCU77=os.environ['DB_PORT_IONESCU77']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME_IONESCU77,
        'USER': DB_USER_IONESCU77,
        'PASSWORD': DB_PASS_IONESCU77,
        'HOST': '127.0.0.1',
        'PORT': DB_PORT_IONESCU77,
    }
}
