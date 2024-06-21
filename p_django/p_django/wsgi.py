import os, sys
sys.path.insert(0, '/var/www/u2701628/data/www/buzticketk.online/p_django')
sys.path.insert(1, '/var/www/u2701628/data/djangoenv/lib/python3.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'p_django.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
