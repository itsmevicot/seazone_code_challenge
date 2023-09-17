SECRET_KEY = 'django-insecure-u#xpmd(!ck4m9+4m3bejuwdtqhkfgkw7hp42wfe@#f=)&1@_yb'

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'seazone_code_challenge',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
