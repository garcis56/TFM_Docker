import os
import django_heroku

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATH = 'C:\Program Files\PostgreSQL\12\bin'
DEBUG_VALUE = 'True'
PGNAME = 'databasedotty'
PGPASSWORD = 'gameschat'
PGUSER = 'postgres'
SECRET_KEY = 'fbfe4e4174753c1d7bf054a2620e9c54'

SECRET_KEY = 'fbfe4e4174753c1d7bf054a2620e9c54'

DEBUG = 'True'

ALLOWED_HOSTS = ['localhost', 'talkjs-django-example.herokuapp.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'games.apps.GamesConfig',
    'users.apps.UsersConfig',
    'crispy_forms',
    'conversations.apps.ConversationsConfig',
    'talkjs.apps.TalkjsConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'gameschat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'gameschat.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'databasedotty',
        'USER': 'postgres',
        'PASSWORD': 'gameschat'
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'games'
LOGIN_URL = 'login'

TALKJS_APP_ID = 'tOWgW8ua'
TALKJS_API_SECRET = 'sk_test_CypPjiGEdNuJnQUAhqFuYVx6'
TALKJS_API_BASE_URL = 'https://api.talkjs.com/v1/'

django_heroku.settings(locals())
