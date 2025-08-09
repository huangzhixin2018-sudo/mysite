"""
Django WSGI配置 - 使用Dummy数据库引擎
"""

import os
import sys
from pathlib import Path

# 添加项目路径
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# 设置环境变量（允许从vercel.json覆盖）
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
if 'DATABASE_URL' not in os.environ:
    os.environ['DATABASE_URL'] = 'dummy://localhost:5432/dummy'
if 'DEBUG' not in os.environ:
    os.environ['DEBUG'] = 'False'
if 'SECRET_KEY' not in os.environ:
    os.environ['SECRET_KEY'] = 'dummy-key-for-testing-only'
if 'ALLOWED_HOSTS' not in os.environ:
    os.environ['ALLOWED_HOSTS'] = '*'

# 导入Django
import django
django.setup()

# 获取Django WSGI应用
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# 兼容性
app = application
