# -*- coding: utf-8 -*-
#
#       Copyright 2010 Yegor Kowalew <kw@sdesign.com.ua>
#
# Django settings for vstatuse project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Yegor Kowalew', 'kowalew.backup@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'kw.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Kiev'

LANGUAGE_CODE = 'ru'

SITE_ID = 1

USE_I18N = True

MEDIA_URL = 'http://192.168.1.13:8000/stat/'

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = '9#$uo_ifegxfflz+($ct^l&93__kb-g%8o_lb4ge$%fo*(nzgy'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)

ROOT_URLCONF = 'vstatuse.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'vstatuse.status',
    'vstatuse.customuser',
)

AUTHENTICATION_BACKENDS = (
    'customuser.auth_backends.CustomUserModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

CUSTOM_USER_MODEL = 'customuser.CustomUser'

OS_WER = 'L'

if OS_WER == 'W':
    MEDIA_ROOT = 'C:/projects/an/stat/'
    TEMPLATE_DIRS = (
    'C:/projects/an/templates'
    )
    ROOT_URLCONF = 'kwblog.urls'
else:
    MEDIA_ROOT = '/home/yegor/Work/Django/vstatuse/stat/'
    TEMPLATE_DIRS = (
    '/home/yegor/Work/Django/vstatuse/templates'
    )
    ROOT_URLCONF = 'vstatuse.urls'

site_dtoolbar = True
#site_dtoolbar = False
INTERNAL_IPS = ('192.168.1.13',)
if site_dtoolbar:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.cache.CacheDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )
    DEBUG_TOOLBAR_CONFIG = {
        #'EXCLUDE_URLS': ('/admin',), # не работает, но в разработке есть...
        'INTERCEPT_REDIRECTS': False,
    }
