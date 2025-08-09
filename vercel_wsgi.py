import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# 导入Django应用
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel需要这个变量名
app = application
