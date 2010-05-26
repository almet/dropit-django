import os.path
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT_PATH, 'staticfiles')
MEDIA_URL = '/site_media/'
ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = '0#=s4i-c@^tm#*sk15%9hxhf$rwm6+$n3i$*)tbzv3*$6&$wzn'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'dropit.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'couchdbkit.ext.django',
    'notes',
)

COUCHDB_DATABASES = (
    ('notes', 'http://127.0.0.1:5984/dropit'),
)

NOTES_FORMATS = (
    ('markdown','Markdown'), 
    ('fulltext','Full Text'), 
    ('rst', 'ReSTructured Text')
)

try:
    from local_settings import *
except:
    pass
DATABASE_ENGINE = "sqlite3"
DATABASE_NAME = "db.sql"
