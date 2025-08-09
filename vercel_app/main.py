"""
Vercel Python运行时入口点 - 纯静态网站模式
"""

import os
import sys
from pathlib import Path

# 添加项目路径
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def handler(request, context):
    """Vercel Python运行时入口点"""
    try:
        # 延迟导入Django，避免每次请求都初始化
        if 'DJANGO_SETTINGS_MODULE' not in os.environ:
            os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
        
        # 导入Django
        import django
        django.setup()
        
        # 导入视图函数
        from mysite.minimal_test_views import welcome_page, health_check, system_info, api_test
        
        path = request.get('path', '/')
        method = request.get('method', 'GET')
        
        # 路由分发
        if path == '/':
            response = welcome_page(None)
        elif path == '/test/health/':
            response = health_check(None)
        elif path == '/test/system/':
            response = system_info(None)
        elif path == '/test/api/':
            response = api_test(None)
        else:
            # 404页面
            return {
                'statusCode': 404,
                'body': '<h1>页面未找到</h1><p>404 - 页面不存在</p>',
                'headers': {'Content-Type': 'text/html; charset=utf-8'}
            }
        
        # 获取响应内容
        if hasattr(response, 'content'):
            body = response.content.decode('utf-8')
        else:
            body = str(response)
        
        # 获取响应头
        headers = {'Content-Type': 'text/html; charset=utf-8'}
        if hasattr(response, 'headers'):
            for key, value in response.headers.items():
                headers[key] = value
        
        return {
            'statusCode': 200,
            'body': body,
            'headers': headers
        }
        
    except Exception as e:
        # 返回错误页面
        import traceback
        error_trace = traceback.format_exc()
        return {
            'statusCode': 500,
            'body': f'<h1>服务器错误</h1><p>{str(e)}</p><pre>{error_trace}</pre>',
            'headers': {'Content-Type': 'text/html; charset=utf-8'}
        }

# Vercel Python运行时要求
app = handler
