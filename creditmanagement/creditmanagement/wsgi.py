"""
WSGI config for creditmanagement project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
# import sys 
# sys.path.append('/Desktop/Final Credit')
# sys.path.append('/Desktop/Final Credit/creditmanagement')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'creditmanagement.settings')

application = get_wsgi_application()
