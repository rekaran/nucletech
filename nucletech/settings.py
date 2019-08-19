"""
Django settings for nucletech project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '624m7xrg%#et&!qi)l*+^=u)gqxau9!w%m8^(+dbo@kp#42%dy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["www.nucletech.com"]

# CSRF headers settings

# CSRF_HEADER_NAME = "HTTP_X_NUCLETECH_TOKEN"
# CSRF_COOKIE_NAME = "nucletechtoken"
# CSRF_COOKIE_DOMAIN = "nucletech.com"
# CSRF_COOKIE_SECURE = True # In Prod

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'home.apps.HomeConfig', # Will contain all non-login pages, single page Vue application.
    'builder.apps.BuilderConfig', # A platform to create and manage the bot.
    'human.apps.HumanConfig', # A platform to manage unhandled queries by a agent.
    'analytics.apps.AnalyticsConfig', # A platform to track the performance of the bot.
    'bot.apps.BotConfig', # A place where the clients can view the demo of multiple types of bot.
    'datamanager.apps.DatamanagerConfig', # Will manage the data of the project that need to be loaded while client/browser loads the script, will authenticate the token that gets refreshed daily in resource manager that can be managed from builder and the domain from which the request is been made, and send the enc. data and token as a response to the browser. It will also manage both SQL and MongoDb data.
    'resourcemanager.apps.ResourcemanagerConfig', # Will manage the files of projects, with tokens and urls inside the file and obfuscate them while loading it and various setting can be managed from builder.
    'api.apps.ApiConfig', # A platform where all the API will published for the user to use with demo and endpoints like Pipedrive.
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'nucletech.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'nucletech.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASE_URL="mongodb://nt-test:cqEu8v4Un6VimhVo@nt-test-shard-00-00-0tdov.mongodb.net:27017,nt-test-shard-00-01-0tdov.mongodb.net:27017,nt-test-shard-00-02-0tdov.mongodb.net:27017/test?ssl=true&replicaSet=nt-test-shard-0&authSource=admin&retryWrites=true&w=majority" # Dev
# DATABASE_URL="mongodb://nt-user:wAQ9mC2f1xjEoXpi@nt-test-shard-00-00-0tdov.mongodb.net:27017,nt-test-shard-00-01-0tdov.mongodb.net:27017,nt-test-shard-00-02-0tdov.mongodb.net:27017/admin?replicaSet=nt-test-shard-0" # Prod


# Authentication Model

AUTH_USER_MODEL = 'home.User'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Password validation karan@nucletech.com: !nfamousSpeed@1012
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


# Login/Logout redirect/url

LOGIN_REDIRECT_URL = 'builder.index'
LOGOUT_REDIRECT_URL = 'home.index'
LOGIN_URL = 'home.login'

# Emailing server setup
# Temporary Email Server :  python -m smtpd -n -c DebuggingServer loaclhost:1025

EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

# Social/Auth

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "726356325527-c4ut01vuoevgn36cbtrl925u2d9q6bqm.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "fQvVhkzRdteF1uKARXuPy06h"

SOCIAL_AUTH_GITHUB_KEY = "d47bf4bb6e8c0f7698f2"
SOCIAL_AUTH_GITHUB_SECRET = "7a62a4203797fd3acc942064b4930a9087ee481b"

SOCIAL_AUTH_FACEBOOK_KEY = "2529859170399458"
SOCIAL_AUTH_FACEBOOK_SECRET = "6cff0838ece187915f9e05947f608436"