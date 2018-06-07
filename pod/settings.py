"""
Django global settings for pod_project.

Django version : 1.11.10.
"""
import os
from pod.main.settings import BASE_DIR
from pod.main.settings import TEMPLATE_THEME

##
# Version of the project
#
VERSION = '2.0.0'

##
# Installed applications list
#
INSTALLED_APPS = [
    # put in first https://github.com/deschler/django-
    # modeltranslation/issues/408 AND http://django-modeltranslation.
    # readthedocs.io/en/latest/installation.html#installed-apps
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    # Exterior Applications
    'ckeditor',
    'sorl.thumbnail',
    'tagging',
    'django_cas',
    'captcha',
    'progressbarupload',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    # Pod Applications
    'pod.main',
    'pod.authentication',
    'pod.filepicker',
    'pod.video',
    'pod.completion',
    'pod.chapters',
    'pod.enrichment',
    'pod.playlist',
    'pod.video_search',
]

##
# Activated middleware components
#
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Pages statiques
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'django_cas.backends.CASBackend',
)

##
# Full Python import path to root URL file
#
ROOT_URLCONF = 'pod.urls'

##
# Full Python path of WSGI app object Django's built-in-servers
# (e.g. runserver) will use
#
WSGI_APPLICATION = 'pod.wsgi.application'

##
# Settings for all template engines to be used
#
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'theme', TEMPLATE_THEME, 'templates'),
            os.path.join(BASE_DIR, 'main', 'templates'),
            os.path.join(BASE_DIR, 'main', 'templates', 'flatpages'),
            os.path.join(BASE_DIR, 'completion', 'templates'),
            os.path.join(BASE_DIR, 'enrichment', 'templates'),
            os.path.join(BASE_DIR, 'playlist', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Local contexts
                'pod.main.context_processors.context_settings',
                'pod.main.context_processors.context_navbar'
            ],
        },
    },
]

##
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': "django.contrib.auth.password_validation.{0}".format(validator)}
    for validator in [
        'UserAttributeSimilarityValidator',
        'MinimumLengthValidator',
        'CommonPasswordValidator',
        'NumericPasswordValidator',
    ]
]

##
# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

##
# Time zone support is enabled (True) or not (False)
#
USE_TZ = True

##
# WEBservices with rest API
#
# curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token
# 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.PageNumberPagination'),
    'PAGE_SIZE': 12
}


##
# Logging configuration https://docs.djangoproject.com/fr/1.11/topics/logging/
#
LOG_DIRECTORY = os.path.join(BASE_DIR, 'log')
if not os.path.exists(LOG_DIRECTORY):
    os.mkdir(LOG_DIRECTORY)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            # 'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'pod/log/django.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'pod.*': {
            'handlers': ['file', 'console', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

##
# Applications settings (and settings locale if any)
#
# Add settings
for application in INSTALLED_APPS:
    if application.startswith('pod'):
        path = application.replace('.', os.path.sep) + '/settings.py'
        if os.path.exists(path):
            _temp = __import__(application, globals(), locals(), ['settings'])
            for variable in (dir(_temp.settings)):
                if variable == variable.upper():
                    locals()[variable] = getattr(_temp.settings, variable)
# add local settings
for application in INSTALLED_APPS:
    if application.startswith('pod'):
        path = application.replace('.', os.path.sep) + '/settings_local.py'
        if os.path.exists(path):
            _temp = __import__(application, globals(),
                               locals(), ['settings_local'])
            for variable in (dir(_temp.settings_local)):
                if variable == variable.upper():
                    locals()[variable] = getattr(
                        _temp.settings_local, variable)
##
# AUTH CAS
#
try:
    if USE_CAS is True:
        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'django_cas.backends.CASBackend',
        )
        CAS_RESPONSE_CALLBACKS = (
            'pod.authentication.populatedCASbackend.populateUser',
            # function call to add some information to user login by CAS
        )
        MIDDLEWARE.append('django_cas.middleware.CASMiddleware')
except NameError:
    pass
