"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``app``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# 强制设置Dummy模式设置（用于Vercel部署测试）
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings_dummy'

# 设置Dummy数据库URL
os.environ['DATABASE_URL'] = 'dummy://localhost:5432/dummy'

app = get_wsgi_application()
