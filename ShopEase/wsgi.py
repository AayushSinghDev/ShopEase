"""
WSGI config for ShopEase — PythonAnywhere
"""
import os
import sys

# PythonAnywhere pe project path add karo
path = '/home/shopease-aks/shopease_final'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ShopEase.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
