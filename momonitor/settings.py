#################
##
## Momonitor Django Settings
##
#################

####
# Section 1. Django Defaults. Don't worry about these. Configurable settings in Section 2
####
from sys import path
from os import environ
from os.path import abspath, basename, dirname, join, normpath
from memcacheify import memcacheify
from postgresify import postgresify


TIME_ZONE = 'UTC'

SITE_ID = 1
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True


# MEDIA CONFIGURATION
dir_path = normpath(dirname(abspath(__file__)))
MEDIA_ROOT = '%s/media/' % dir_path
MEDIA_URL = '/media/'
# END MEDIA CONFIGURATION


# TEMPLATE CONFIGURATION
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = '%s/common/templates/' % dir_path
# END TEMPLATE CONFIGURATION


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'breadcrumbs.middleware.BreadcrumbsMiddleware',
)

ROOT_URLCONF = 'momonitor.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.humanize',
    'south',
    'momonitor.main',
    'momonitor.common',
    'momonitor.slideshow',
    'momonitor.mobile',
    'breadcrumbs',
    'social_auth',
    'storages',
    'gunicorn'
)


TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.tz",
                               "django.contrib.messages.context_processors.messages",
                               'django.core.context_processors.request',
                               'momonitor.common.context_processors.service_endpoints')

#Email the admins if momonitor ever breaks
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

#This is the global endpoint that pagerduty uses for custom events.
PAGERDUTY_ENDPOINT = "https://events.pagerduty.com/generic/2010-04-15/create_event.json"
LOGIN_URL = '/social_auth/login/google/'

#Add media to the python path so that we can run code checks in the media/uploaded_scripts directory
import sys
sys.path.insert(0,normpath(join(dirname(abspath(__file__)) ,'media')))

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.google.GoogleBackend',
    'django.contrib.auth.backends.ModelBackend'
)

FAKE_APP_PORT = 5000
FAKE_APP_HOST = "localhost"
IS_TESTING = sys.argv[1:2] == ['test']


####
# Section 2. Configurable Settings
####


DEBUG=False
TEMPLATE_DEBUG = DEBUG


CHECK_MODELS = []


if IS_TESTING:
    UMPIRE_ENDPOINT = "http://%s:%s/check" % (FAKE_APP_HOST,FAKE_APP_PORT)
    SENSU_API_ENDPOINT = "http://%s:%s" % (FAKE_APP_HOST,FAKE_APP_PORT)
    GRAPHITE_ENDPOINT = "http://%s:%s" % (FAKE_APP_HOST,FAKE_APP_PORT)

    #this will make tests not work
    if CHECK_MODELS:
        del CHECK_MODELS

else:
    #If you are using external service, set their endpoints above
    UMPIRE_ENDPOINT = environ.get('UMPIRE_ENDPOINT', '')
    SENSU_API_ENDPOINT = environ.get('SENSU_API_ENDPOINT', '')
    GRAPHITE_ENDPOINT = environ.get('GRAPHITE_ENDPOINT', '')

    
#OAuth rule. Only allow people with a google email ending in 'example.org' to access the site
GOOGLE_WHITE_LISTED_DOMAINS = [environ.get('GOOGLE_WHITE_LISTED_DOMAINS', '')]


# Set this to the Domain of the site that will be hosting momonitor.
# This will be used to create links in emails sent from momonitor. 
# Use 'http://localhost' for testing
DOMAIN = environ.get('DOMAIN', 'http://localhost')


SECRET_KEY = environ.get('SECRET_KEY', '')


# EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = environ.get('MANDRILL_USERNAME', '')
EMAIL_HOST_PASSWORD = environ.get('MANDRILL_APIKEY', '')
EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.mandrillapp.com')
EMAIL_PORT = environ.get('EMAIL_PORT', 587)
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER
# END EMAIL CONFIGURATION


# DATABASE CONFIGURATION
DATABASES = postgresify()
# END DATABASE CONFIGURATION


# CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = memcacheify()
# END CACHE CONFIGURATION


# AWS STORAGE CONFIGURATION
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', 'default-storage')
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_EXPIREY = 60 * 60 * 24 * 7
AWS_HEADERS = {
    'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIREY,
                                                                   AWS_EXPIREY)
                                                                   }
# END AWS STORAGE CONFIGURATION


# STATICFILE CONFIGURATION
STATIC_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
STATIC_ROOT = '%s/common/upload/' % dir_path
STATICFILES_DIRS = (
    '%s/common/static/' % dir_path,
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
# END STATICFILE CONFIGURATION


# SERVICE CHECK CONFIGURATION
UMPIRE_USER = environ.get('UMPIRE_USER', '')
UMPIRE_API = environ.get('UMPIRE_API', '')
GRAPHITE_USER = environ.get('GRAPHITE_USER', '')
GRAPHITE_API = environ.get('GRAPHITE_API', '')
# END SERVICE CHECK CONFIGURATION
