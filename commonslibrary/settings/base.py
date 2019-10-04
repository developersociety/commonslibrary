"""
Django settings for commonslibrary project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Production / development switches
# https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

# Email
# https://docs.djangoproject.com/en/1.11/ref/settings/#email

ADMINS = (('Developer Society', 'studio@dev.ngo'),)
MANAGERS = ADMINS

SERVER_EMAIL = 'commonslibrary@devsoc.org'
DEFAULT_FROM_EMAIL = 'librarian@the-open.net'
EMAIL_SUBJECT_PREFIX = '[commonslibrary] '

PROJECT_APPS_ROOT = os.path.join(BASE_DIR, 'apps')
sys.path.append(PROJECT_APPS_ROOT)

DEFAULT_APPS = [
    # These apps should come first to load correctly.
    'blanc_admin_theme',
    'core',
    'django.contrib.admin.apps.AdminConfig',
    'django.contrib.auth.apps.AuthConfig',
    'django.contrib.contenttypes.apps.ContentTypesConfig',
    'django.contrib.sessions.apps.SessionsConfig',
    'django.contrib.messages.apps.MessagesConfig',
    'django.contrib.staticfiles.apps.StaticFilesConfig',
    'django.contrib.sites.apps.SitesConfig',
]

THIRD_PARTY_APPS = [
    'ckeditor',
    'ckeditor_uploader',
    'colorfield',
    'crispy_forms',
    'django_filters',
    'django_mptt_admin',
    'maskpostgresdata',
    'mptt',
    'raven.contrib.django.apps.RavenConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'sorl.thumbnail',
    'adminsortable',
]

PROJECT_APPS = [
    'accounts.apps.AccountsConfig',
    'api.v1.apps.ApiConfig',
    'comments.apps.CommentsConfig',
    'directory.apps.DirectoryConfig',
    'future.apps.FutureConfig',
    'pages.apps.PagesConfig',
    'resources.apps.ResourcesConfig',
    'tags.apps.TagsConfig',
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'pages.middleware.PageFallbackMiddleware',
]

ROOT_URLCONF = 'commonslibrary.urls'

WSGI_APPLICATION = 'commonslibrary.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(),
}

# Caches
# https://docs.djangoproject.com/en/1.11/topics/cache/

CACHES = {}
if os.environ.get('MEMCACHED_SERVERS'):
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': os.environ['MEMCACHED_SERVERS'].split(' '),
        'KEY_PREFIX': os.environ.get('MEMCACHED_PREFIX'),
    }
else:
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = False

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = os.environ.get('STATIC_URL', '/static/')

STATIC_ROOT = os.path.join(BASE_DIR, 'htdocs/static')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# File uploads
# https://docs.djangoproject.com/en/1.11/ref/settings/#file-uploads

MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')

MEDIA_ROOT = os.path.join(BASE_DIR, 'htdocs/media')

DEFAULT_FILE_STORAGE = os.environ.get(
    'DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage'
)

# Templates
# https://docs.djangoproject.com/en/1.11/ref/settings/#templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'directory.context_processors.footer_orgs',
                'core.context_processors.demo',
                'resources.context_processors.resource_categories',
            ],
        },
    },
]

# Logging
# https://docs.djangoproject.com/en/1.11/topics/logging/#configuring-logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        }
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'formatter': 'django.server',
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'elasticapm.errors': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'elasticapm.transport': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'raven': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'sentry.errors': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'sorl.thumbnail': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Sites framework
SITE_ID = 1

# Thumbnail generation
THUMBNAIL_PREFIX = 'thumbs/'
THUMBNAIL_PRESERVE_FORMAT = True
THUMBNAIL_QUALITY = 100

# Cloud storage
CONTENTFILES_PREFIX = os.environ.get('CONTENTFILES_PREFIX', 'commonslibrary')
CONTENTFILES_HOSTNAME = os.environ.get('CONTENTFILES_HOSTNAME')
CONTENTFILES_SSL = True

# Improved cookie security
CSRF_COOKIE_HTTPONLY = True

DEMO_SITE = False

AUTH_USER_MODEL = 'accounts.User'

# yapf: disable
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono-lisa',
        'toolbar_Basic': [['Source', '-', 'Bold', 'Italic']],
        'toolbar': [{
            'name': 'basicstyles',
            'items': [
                'Format', '-', 'Bold', 'Italic', 'Underline', 'Strike', '-', 'Image', 'Link',
                'Source', '-', 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-',
                'JustifyLeft', 'JustifyCenter', 'JustifyRight', '-', 'Youtube', '-', 'MJAccordion',
            ],
        }],
        'extraPlugins': ','.join(['youtube', 'widget', 'lineutils', 'mjAccordion']),
        'contentsCss': ','.join(['/static/src/admin/css/ckeditor_accordion.css']),
        'allowedContent': True,
        'mjAccordion_managePopupTitle': False,
        'mjAccordion_managePopupContent': False,
        'mj_variables_allow_html': True,
    }
}
CKEDITOR_UPLOAD_PATH = 'ckeditor_uploads/'
# yapf: enable

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}
