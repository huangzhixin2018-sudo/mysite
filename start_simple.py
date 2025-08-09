#!/usr/bin/env python3
"""
简化的Django启动脚本 - 避免复杂配置
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# 设置环境变量
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
os.environ['DEBUG'] = 'False'

try:
    import django
    django.setup()
    
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    print("✅ Django启动成功")
    
except Exception as e:
    print(f"❌ Django启动失败: {e}")
    
    # 返回简单的错误处理函数
    def application(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, response_headers)
        
        error_html = f"""
        <html>
        <body>
            <h1>Django启动失败</h1>
            <p>错误: {str(e)}</p>
            <p>请检查配置和依赖</p>
        </body>
        </html>
        """
        return [error_html.encode('utf-8')]

if __name__ == '__main__':
    print("Django应用已准备就绪")
