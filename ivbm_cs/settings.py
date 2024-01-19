"""
Django settings for ivbm_cs project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*8+-90(p)j852f6w=2!sk7$op1nxh%ipkoxs@-l@^*8rj^gb^@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    #'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'admin_panel',
]





MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ivbm_cs.urls'

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'





TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'ivbm_cs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

#DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		#'NAME': 'ivbmcs_db_3',
		'NAME': 'ivbmcs_db',
		'USER': 'root',
		'PASSWORD': '1234',
		'HOST':'localhost',
		'PORT':'3306',
        'TIME_ZONE' :  'Asia/Kolkata'
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE =  'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
STATIC_ROOT = os.path.join(BASE_DIR,'assets')


# MEDIA_URL = 'media/'
# MEDIA_ROOT = os.path.join(BASE_DIR,'media') 
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# settings.py

TWILIO_ACCOUNT_SID = 'ACea07b1ac009276f9122f2b841e54145d'
TWILIO_AUTH_TOKEN = '403ec04c5e46b98fc2b6a3e30b5b69fd'
TWILIO_PHONE_NUMBER = '8848496707'



SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # or 'django.contrib.sessions.backends.cache', etc.
SESSION_COOKIE_AGE = 1209600

# LOGIN_URL = ':login'  # Adjust this to match your login URL
MEDIA_ROOT = os.path.join(BASE_DIR, 'images')
MEDIA_URL = '/images/'


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Use the appropriate port for your email server
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'vasudevankarthik9@gmail.com'
EMAIL_HOST_PASSWORD = 'jdaz ahrr xngs ozqa'
#EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# print(f'EMAIL_HOST_PASSWORD: {EMAIL_HOST_PASSWORD}')

# for key, value in os.environ.items():
#     print(f'{key}: {value}')