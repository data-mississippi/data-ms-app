# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

from app.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mi7+sor%@+xus-q*r)-oiay_3*00l$p%32dq(_n+#9*y7-bz(#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'backend',
    'localhost'
]