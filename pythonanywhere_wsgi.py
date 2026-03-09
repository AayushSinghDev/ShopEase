# This file goes to: /var/www/aks000_pythonanywhere_com_wsgi.py
import sys
import os

path = '/home/aks000/ShopEase'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ShopEase.settings_production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
