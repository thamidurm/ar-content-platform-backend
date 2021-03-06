"""
Django settings for ar_platform project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os,sys
import mongoengine

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config( 
  cloud_name = "db2rl2mxy", 
  api_key = "334545739998458", 
  api_secret = "RRESEbJtwrppkSEab5AlDVGZR9w" 
)   

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c$5t)yhkbg=yez8d)+(5rpqvp&29wu&0)9p-gql+-lkj=e%#-y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
'ar-content-platform-backend.herokuapp.com',
'localhost'
]



# Application definitions

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_mongoengine',
    'app',
    'creators',
    'file_manager',
    'cloudinary',
    'moderators'
]

CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
]
# STATICFILES_STORAGE ='ar_platform.storage.WhiteNoiseStaticFilesStorage'

ROOT_URLCONF = 'ar_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # <- add this line
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

WSGI_APPLICATION = 'ar_platform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # 'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'd8f4ccoc8cg552',
        'USER': 'yrbpmcnnvitdjr',
        'PASSWORD': '651957d666616702e7315ba09a262b51dcd9b2007a6ad590d103df65d1fbb5f2',
        'HOST': 'ec2-46-137-156-205.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}

if 'test' in sys.argv or 'test_coverage' in sys.argv: #Covers regular testing and django-coverage
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'


MONGODB_DATABASES = {
    "default": {
        "name": "test",
        "host": "localhost",
        "port": 27017,
        "tz_aware": True,  # if you use timezones in django (USE_TZ = True)
    },

    "test": {
        "name": "automated_tests",
        "host": "localhost",
        "port": 27017,
        "tz_aware": True,  # if you use timezones in django (USE_TZ = True)
    }
}


def is_test():
    """
    Checks, if we're running the server for real or in unit-test.
    We might need a better implementation of this function.
    """
    if 'test' in sys.argv or 'testserver' in sys.argv:
        print("Using a test mongo database")
        return True
    else:
        # print("Using a default mongo database")
        return False

if is_test():
    db = 'test'
    mongoengine.connect(
        'testdb',
        host='mongomock://localhost'
        )
    conn = mongoengine.get_connection()
else:
    db = 'default'
    mongoengine.connect(
    db=MONGODB_DATABASES[db]['name'],
    # host ='localhost',
    username='dbuser',
    password='lKDrviFTSBqCTskC',
    host='mongodb+srv://dbuser:lKDrviFTSBqCTskC@cluster0-tvuyt.mongodb.net/'+ MONGODB_DATABASES[db]['name'] +'?retryWrites=true&w=majority'
)




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
AUTH_USER_MODEL = 'moderators.Moderator'

# AUTH_USER_MODEL = 'creators.Creator'

MONGOENGINE_USER_DOCUMENT = 'creators.models.Creator'

# Don't confuse Django's AUTHENTICATION_BACKENDS with DRF's AUTHENTICATION_CLASSES!
AUTHENTICATION_BACKENDS = (
    'creators.authentication.CreatorAuthBackend',
    'django.contrib.auth.backends.ModelBackend'
   
    # 'mongoengine.django.auth.MongoEngineBackend',
    
)

DEFAULT_AUTHENTICATION_CLASSES = (
    'creators.authentication.TokenAuthentication',
    'rest_framework.authentication.SessionAuthentication',
)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
#STATIC_ROOT = '/static/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
