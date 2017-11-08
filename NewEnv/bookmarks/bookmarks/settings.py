"""
Django settings for bookmarks project.

Generated by 'django-admin startproject' using Django 1.8.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.core.urlresolvers import reverse_lazy




BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%4mulu)vvot8_e&#(gg5g(wnjd)is#!6bm=81p8fz%#adbq^b('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail',args=[u.username])
}


LOGIN_REDIRECT_URL = reverse_lazy('dashboard')
LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0



# Email configuration

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'paypal.standard.ipn',
    'sorl.thumbnail',
    'images',
    'actions',
    'courses',
    'account',
    'shop',
    'cart',
    'orders',
    'payment',
    'weasyprint',
    'coupons',
    # 'rosetta',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    

)

ROOT_URLCONF = 'bookmarks.urls'

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
                'cart.context_processors.cart',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',

            ],
        },
    },
]

WSGI_APPLICATION = 'bookmarks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en' 
# LANGUAGES = (
#     ('en', _('english')),
#     ('es', _('spanish')),
#     )
# LOCALE_PATHS = (
#     os.path.join(BASE_DIR, 'locale/'),
#     )

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR,'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

AUTHENTICATION_BACKENDS = (
                
                
                'social.backends.google.GoogleOAuth2',
                'social.backends.facebook.Facebook2OAuth2',
                'social.backends.twitter.TwitterOAuth',
                'django.contrib.auth.backends.ModelBackend',
                'account.authentication.EmailAuthBackend',)

SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_FACEBOOK_KEY = '233156223724412' # Facebook App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'b6a2407cefde906313fe76b94ce5f166' # Facebook App Secret
#SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']   #Facebook Scope
SOCIAL_AUTH_TWITTER_KEY = '' #Twitter consumer key
SOCIAL_AUTH_TWITTER_SECRET = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='767674675436-s3lrmchrhe1nigbqdfv011h88l9pe025.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET ='kkUTaBitRE7xqirZk8Zjronv'
#SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'complete/facebook'

# django-paypal settings
PAYPAL_RECEIVER_EMAIL = 'paddypopeye@hotmail.com'
PAYPAL_TEST = True
CART_SESSION_ID = 'cart'

CELERY_IMPORTS = ("tasks", )
CELERY_RESULT_BACKEND = "amqp"
BROKER_URL = "amqp://guest:guest@localhost:5672//"
CELERY_TASK_RESULT_EXPIRES = 300

print ("this base dir ",BASE_DIR)

print ("this is STATIC_ROOT", STATIC_ROOT)

print ("this is MEDIA_ROOT", MEDIA_ROOT)
