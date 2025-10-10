import os
import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

# Expose the app instance for Vercel
from api.wsgi import application

def handler(request, *args, **kwargs):
    return application(request, *args, **kwargs)
