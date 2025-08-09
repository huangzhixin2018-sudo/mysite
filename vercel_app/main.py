"""
Django WSGI配置 - 使用Dummy数据库引擎
"""

import os
import sys
from pathlib import Path

# 添加项目路径
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# 强制设置环境变量
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings_dummy'
os.environ['DATABASE_URL'] = 'dummy://localhost:5432/dummy'
os.environ['DEBUG'] = 'False'
os.environ['SECRET_KEY'] = 'dummy-key-for-testing-only'
os.environ['ALLOWED_HOSTS'] = '*'

# 导入Django
import django
django.setup()

# 获取Django WSGI应用
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# 兼容性
app = application
