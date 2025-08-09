"""
测试视图 - 不依赖数据库
用于验证基础功能是否正常
"""

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
import platform

@csrf_exempt
def health_check(request):
    """健康检查接口"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Django项目运行正常',
        'timestamp': __import__('datetime').datetime.now().isoformat()
    })

@csrf_exempt
def system_info(request):
    """系统信息接口"""
    return JsonResponse({
        'python_version': platform.python_version(),
        'django_version': __import__('django').get_version(),
        'platform': platform.platform(),
        'environment': os.environ.get('DJANGO_SETTINGS_MODULE', 'unknown'),
        'debug': os.environ.get('DEBUG', 'unknown')
    })

@csrf_exempt
def static_test(request):
    """静态资源测试页面"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 Django部署测试页面</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .status { padding: 15px; margin: 10px 0; border-radius: 5px; }
            .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            .warning { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }
            .info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
            .code { background: #f8f9fa; padding: 10px; border-radius: 3px; font-family: monospace; }
            .button { display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 5px; }
            .button:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Django项目部署成功！</h1>
            
            <div class="status success">
                <h3>✅ 基础功能测试通过</h3>
                <p>项目已成功部署到Vercel，基础环境配置正常。</p>
            </div>
            
            <div class="status info">
                <h3>📊 当前状态</h3>
                <ul>
                    <li><strong>环境配置:</strong> ✅ 正常</li>
                    <li><strong>静态资源:</strong> ✅ 正常</li>
                    <li><strong>路由系统:</strong> ✅ 正常</li>
                    <li><strong>数据库连接:</strong> ❌ 待解决（使用Dummy数据库）</li>
                </ul>
            </div>
            
            <div class="status warning">
                <h3>⚠️ 下一步操作</h3>
                <p>当前使用Dummy数据库模式，需要解决PostgreSQL连接问题：</p>
                <ol>
                    <li>检查Supabase网络访问策略</li>
                    <li>验证连接字符串和SSL配置</li>
                    <li>测试数据库连接</li>
                    <li>切换到真实数据库配置</li>
                </ol>
            </div>
            
            <h3>🔧 测试接口</h3>
            <a href="/test/health/" class="button">健康检查</a>
            <a href="/test/system/" class="button">系统信息</a>
            
            <h3>📝 技术细节</h3>
            <div class="code">
                <strong>当前配置:</strong> mysite.settings_dummy<br>
                <strong>数据库引擎:</strong> django.db.backends.dummy<br>
                <strong>部署平台:</strong> Vercel<br>
                <strong>状态:</strong> 基础功能测试模式
            </div>
            
            <hr>
            <p><em>这是一个测试页面，用于验证Django项目的基础部署是否成功。</em></p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

@csrf_exempt
def api_test(request):
    """API测试接口"""
    if request.method == 'GET':
        return JsonResponse({
            'method': 'GET',
            'message': 'API接口正常工作',
            'data': {
                'test': True,
                'database_mode': 'dummy',
                'status': 'deployed'
            }
        })
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            return JsonResponse({
                'method': 'POST',
                'received_data': data,
                'message': '数据接收成功'
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON data'
            }, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
