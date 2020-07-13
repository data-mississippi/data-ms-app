"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.base')
print('wsgi.py')
print(os.environ.get('DJANGO_SETTINGS_MODULE'))

print(sys.path)

application = get_wsgi_application()
