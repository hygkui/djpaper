# Django settings for djtest project.
import os.path
import string
DEBUG = True
TEMPLATE_DEBUG = DEBUG

################################################
##---start--- custome setting for the project.##
################################################
HERE = os.path.dirname(os.path.abspath(__file__))
DB_USER = 'ghh'
DB_NAME = 'db_test'
DB_PWD = 'ghhpasswd'
CACHE_BACKEND_URL = 'file:///home/ghh/dj/cache_backend?timeout=60&max_entries=400'
APPS_STATICFILES_DIRS = os.path.join(HERE , 'djpaper/static/')
DOMAIN_NAME = 'http://localhost:8000'
################################################
##---end--- custome setting for the project.##
################################################
INSTALLED_APPS = (
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.staticfiles',
   'django.contrib.sites',
   'django.contrib.messages',
   'django.contrib.admin',
##########################################
#####--start--  add your app's names ####
   'djpaper',
#####---end--   add your app's names ####
##########################################
)



################################################
#######  the normal setting as the same. ######
################################################
ADMINS = (
)
MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DB_NAME,                      # Or path to database file if using sqlite3.
        'USER': DB_USER,                      # Not used with sqlite3.
        'PASSWORD': DB_PWD,                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = os.path.join( HERE , 'media').replace('\\','/')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join( HERE,'static').replace('\\','/')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = (
    APPS_STATICFILES_DIRS.replace('\\','/'),
)
SECRET_KEY = '##z=90wf8(h+#+igu13+k1jdtj$uw*t3cyn=)n#_b+4)-r@cxm'
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
)
ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = (
	os.path.join( HERE ,"templates").replace('\\','/'),	
)

LOGIN_REDIRECT_URL='/accounts/profile/'
#CACHE_BACKEND = string.join(['file://',HERE,'dj_cache','?timeout=60&max_entries=400'])
CACHE_BACKEND = CACHE_BACKEND_URL
FILE_UPLOAD_HANDLERS =("django.core.files.uploadhandler.TemporaryFileUploadHandler",)	

TEMPLATE_CONTEXT_PROCESSORS=(
	"django.core.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.media",
	"django.core.context_processors.i18n",
	"django.core.context_processors.request",
)
