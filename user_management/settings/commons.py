"""
Django settings for myJournal project.

Generated by 'django-admin startproject' using Django 2.2.9.
For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import datetime
from sys import path

from configurations import Configuration

# from .logger import LoggerSettingsMixin


class Settings(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # MEDIA_DIR = os.path.join(BASE_DIR, 'media')
    path.append(BASE_DIR)
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'rest_framework_swagger',
        'authentication',
        'base',
        'info'
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

    ROOT_URLCONF = 'user_management.urls'

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

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        )
    }

    WSGI_APPLICATION = 'user_management.wsgi.application'

    AUTH_USER_MODEL = 'authentication.AuthUser'
    AUTHENTICATION_BACKENDS = (
        'user_management.backends.auth_backend.PasswordlessAuthBackend',
    )

    # Database
    # https://docs.djangoproject.com/en/2.2/ref/settings/#databases

    POSTGRES_DB_NAME = os.environ["POSTGRES_DB_NAME"]
    POSTGRES_USER_NAME = os.environ["POSTGRES_USER_NAME"]
    POSTGRES_USER_PASSWORD = os.environ["POSTGRES_USER_PASSWORD"]
    POSTGRES_DB_HOST = os.environ.get("POSTGRES_DB_HOST", 'localhost')
    POSTGRES_DB_PORT = os.environ.get("POSTGRES_DB_PORT", '5432')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': POSTGRES_DB_NAME,
            'USER': POSTGRES_USER_NAME,
            'PASSWORD': POSTGRES_USER_PASSWORD,
            'HOST': POSTGRES_DB_HOST,
            'PORT': POSTGRES_DB_PORT,
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/2.2/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'Asia/Calcutta'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.2/howto/static-files/
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')    
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    STATIC_URL = '/static/'

    # MEDIA_ROOT = MEDIA_DIR
    # MEDIA_URL = '/media/'

    # LOGIN_URL =


    # Project related variables
    # JWT token related settings

    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1000),
        'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1000),
    }

    SIGNUP_TOKEN_VALIDITY = 1800

    OTP_API_KEY = os.environ.get("OTP_API_KEY", "")
    OTP_BASE_URL = os.environ.get("OTP_BASE_URL", "")
