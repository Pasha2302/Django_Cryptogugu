import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from celery.schedules import crontab
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ml!+kdg#45vs*-zzjj1(7^k7uczwrpajf3bm_0(^y6w*bxmzz5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_celery_beat',     # pip install celery django-celery-beat
    'django_celery_results',  # pip install django-celery-results
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    # 'app.middleware.DefaultLanguageMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Для правильной обработки статических файлов Django рекомендуется использовать WhiteNoise:
    # pip install whitenoise
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # file - middleware_check_request.py:
    'core.middleware_check_request.LogLongRequestsMiddleware', # логирование долгих запросов
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cgugu_test',
        'USER': 'pavelpc',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
        'ATOMIC_REQUESTS': True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Russian'),
    ('es', 'Spanish'),
    ('pt', 'Portuguese'),
    ('zh-hans', 'Simplified Chinese'),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


# Включите сжатие (необязательно, но рекомендуется для улучшения производительности) в настройках:
WHITENOISE_USE_FINDERS = True
WHITENOISE_USE_CDN = True

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ================================================================================================================== #

# Периодические задачи Celery
CELERY_BEAT_SCHEDULE = {
    'reset_votes24h_daily': {
        'task': 'app.tasks.reset_votes24h',
        # 'schedule': crontab(hour=0, minute=0),  # Запуск в полночь каждый день
        'schedule': crontab(minute='0'),  # Чтобы выполнить задачу каждый час:
    },
    'auto_voting_every_day': {
        'task': 'app.tasks.auto_voting',
        # 'schedule': crontab(hour=0, minute=0),  # Запуск в полночь каждый день
        # 'schedule': crontab(minute=0),  # Чтобы выполнить задачу каждый час:
        'schedule': crontab(minute='*/30'),
        # Для выполнения задачи каждые 5 минут, можно использовать параметр minute с шагом */5
    },
    'start_update_coins_every_day': {
            'task': 'app.tasks.start_update_coins',
            # 'schedule': crontab(hour=0, minute=0),  # Запуск в полночь каждый день
            # 'schedule': crontab(minute=0),  # Чтобы выполнить задачу каждый час:
            'schedule': crontab(minute='*/10'),
        },
}

# Настройки Celery (нужна библиотека redis - pip install redis)
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

