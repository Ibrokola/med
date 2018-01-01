from __future__ import absolute_import, unicode_literals

from clinic1.aws.conf import *

from decouple import config

from .base import *

DEBUG = False

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = ['clinic1yeg.herokuapp.com',]

INSTALLED_APPS = [

    'storages',
]

try:
    from .local import *
except ImportError:
    pass
