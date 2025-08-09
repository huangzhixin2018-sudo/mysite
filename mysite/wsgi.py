"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``app``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# 强制设置生产环境设置
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings_production'

app = get_wsgi_application()
