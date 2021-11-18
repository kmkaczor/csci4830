"""
Django settings for csci4830 project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

#### SECURITY WARNING: keep the secret key used in production secret! ####

# <!> Prevent secret key from appearing in github. Put the secret key in your home directory pathfolder with the
# <!> .csci4830-secretkey file containing the secret key string. This will search in the home directory of the user
# <!> running apache or django's own web instance, and will let you know exactly where it is looking
# <!> in the log files.

#AWS_DEVEL_DB = "13.58.197.121"
AWS_DEVEL_DB = '3.135.240.54'
# This will use a secret key file in the apache user's home -- in ubuntu this is /var/www
sk_file = str(Path.home()) + "/.csci4830-secretkey"
SECRET_KEY = "THISISTHETEXT"
"""
try:
    print("Using secret key file: " + sk_file)
    SECRET_KEY = open(sk_file, 'r').read()
except Exception as err:
    print("Unable to load secret key file "
          + sk_file + ": " + err.strerror)
    exit(1)


ALLOWED_HOSTS = ["localhost", "127.0.0.1",  # Allow development environment
                 # Korey's AWS instance -- also development database
                 AWS_DEVEL_DB, "ec2-3-16-112-104.us-east-2.compute.amazonaws.com",
                 "3.135.240.54"
                 # Add your AWS here
                 # "0.0.0.0"


                 # <!> Add your server here. You should probably put down both the IP address and the domain name
                 # <!> so that you can access from both methods (apache will notice the difference)
                 ]
"""

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This is the folder that manage.py is in. Thus MEDIA_ROOT and etc are in that folder
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = str(BASE_DIR) + '/files/'
MEDIA_URL = '/files/'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'libraryshop.models',
    # 'libraryshop.apps.*'
    'libraryshop.apps.LibraryshopConfig'
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

ROOT_URLCONF = 'csci4830.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates/'],
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

WSGI_APPLICATION = 'csci4830.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


"""
Replace the DATABASE lines before release -- python's windows mysql implementation legs behind Linux
But this works just as well for development purpose (although no central mysql server for now)
"""

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'CSCI4830project',
#        'USER': 'CSCI4830',
#        'PASSWORD': 'CSCI4830Django',
#        'HOST': AWS_DEVEL_DB,  # "127.0.0.1",
#        'PORT': '3306',
#    },
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "static"
print('sr: ' + str(STATIC_ROOT))

STATICFILES_DIRS = [
    #BASE_DIR / 'static/',
]
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#
# The below options were not created by Django
#

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
