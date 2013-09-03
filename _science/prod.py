'''
Created on 2013-08-27

@author: Ian
'''
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}

ALLOWED_HOSTS = [".underscorescience.com"]

MEDIA_ROOT = '/media/'


STATIC_ROOT = '/static/'

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME ='underscore-science'
DEFAULT_FILE_STORAGE = '_science.s3utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = '_science.s3utils.StaticRootS3BotoStorage'
s3_URL = 'http://%s.s3.amazonaws.com/' %AWS_STORAGE_BUCKET_NAME
STATIC_URL = s3_URL + STATIC_ROOT
MEDIA_URL = s3_URL + MEDIA_ROOT
AWS_QUERYSTRING_AUTH =False

#allows session cookie to apply to all sub domains.
SESSION_COOKIE_DOMAIN=".underscorescience.com"

#prepend ww for seo
PREPEND_WWW = True

