"""
WSGI config for _science project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
#os.environ["DJANGO_SETTINGS_MODULE"] = "_science.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_science.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()

# Apply WSGI middleware here. la lal la
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)

#adding apache environ variables to os.environ
DEBUG = False

def application(environ, start_response):
    if not DEBUG:
        os.environ['RDS_DB_NAME'] = environ["RDS_DB_NAME"]
        os.environ['RDS_USERNAME'] = environ["RDS_USERNAME"]
        os.environ['RDS_PASSWORD'] = environ["RDS_PASSWORD"]
        os.environ['RDS_HOSTNAME'] = environ["RDS_HOSTNAME"]
        os.environ['RDS_PORT'] = environ["RDS_PORT"]
        os.environ['AWS_ACCESS_KEY_ID'] = environ["AWS_ACCESS_KEY_ID"]
        os.environ['AWS_SECRET_ACCESS_KEY'] = environ["AWS_SECRET_ACCESS_KEY"]
        os.environ['AWS_STORAGE_BUCKET_NAME'] = environ["AWS_STORAGE_BUCKET_NAME"]
        os.environ['SECRET_KEY'] = environ["SECRET_KEY"]
    return _application(environ, start_response)



