"""
Django settings for cms project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
# import socket
# try:
#     hostname = socket.gethostname()
# except:
#     hostname = 'default'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x8=ujz!3ioo_hzuj@#tx%3jg_$5c=%(!5jao#@4h+@1o)x^5$i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com', 'bluedjango.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',

    'accounts.apps.AccountsConfig',
    'widget_tweaks',

    # ? plugin
    'django_filters',
    # 'phone_field',

    'livereload',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cms.urls'

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
                'accounts.views.referral_on_all_pages',
                'accounts.views.bank_on_all_pages',
                'accounts.views.game_on_all_pages',
                'accounts.views.activeDate_on_all_page',
                'accounts.views.today_yesterday_display',
            ],
        },
    },
]

FIXTURE_DIRS = [
    'fixtures'
]

WSGI_APPLICATION = 'cms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# live DB
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'd9bukmdbiat1fe',
#         'USER': 'kljlkbdphvpmrc',
#         'PASSWORD': 'c3da0c5c79071b11d7b260070e8978084a6abc6192af013a9f2c1ca49d1a59fb',
#         'HOST': 'ec2-52-204-232-46.compute-1.amazonaws.com',
#         'PORT': '5432',
#     }
# }

# Heroku Postgresql
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'dahsvl30h6qp6b',
#         'USER': 'zjobtbemfgzuxz',
#         'PASSWORD': '4d6fa703d5c2897e140abedbaf303bfce2c4ea4b0027f955c5eaded3eb66b933',
#         'HOST': 'ec2-54-228-250-82.eu-west-1.compute.amazonaws.com',
#         'PORT': '5432',
#     }
# }


# Local Postgre
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django',
        'HOST': 'localhost', 
        'USER': 'postgres', 
        'PASSWORD': 'android19', 
        'PORT': '5432',
    }
}

#Local MySQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'django',
#         'HOST': 'localhost', 
#         'USER': 'django', 
#         'PASSWORD': 'django123!!!', 
#         'PORT': '3306',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#          'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#      }
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
# MEDIA_ROOT  = os.path.join(BASE_DIR, 'media/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles'), ]

# MEDIA_URL = '/static/images/' #for hosting


# #email

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'youremail'
# EMAIL_HOST_PASSWORD = 'yourpassword'

MIDDLEWARE_CLASSES = (
    'accounts.middleware.UserPositionMiddleware',
    'livereload.middleware.LiveReloadScript',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}