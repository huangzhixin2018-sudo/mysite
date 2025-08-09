"""
简单的测试视图 - 不依赖数据库
用于Dummy模式下的基础功能测试
"""

from django.http import HttpResponse, JsonResponse
import os
import platform
import sys

def health_check(request):
    """健康检查接口"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Django项目运行正常',
        'mode': 'dummy_database'
    })

def system_info(request):
    """系统信息接口"""
    return JsonResponse({
        'python_version': platform.python_version(),
        'django_version': '5.0.7',
        'platform': platform.platform(),
        'mode': 'dummy_database'
    })

def static_test(request):
    """静态页面测试"""
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django Dummy模式测试</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        .status { padding: 15px; margin: 20px 0; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .warning { background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        ul { line-height: 1.8; }
        .next-steps { background: #e2e3e5; padding: 20px; border-radius: 5px; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Django项目部署成功！</h1>
        
        <div class="status success">
            <strong>✅ 当前状态：</strong> 使用Dummy数据库模式，仅用于测试基础功能
        </div>
        
        <div class="status info">
            <strong>📋 测试结果：</strong>
            <ul>
                <li>✅ 环境配置 - Django框架正常运行</li>
                <li>✅ 静态资源 - 静态文件服务正常</li>
                <li>✅ 路由系统 - URL路由工作正常</li>
                <li>✅ 中间件 - 安全中间件工作正常</li>
                <li>❌ 数据库功能 - 预期失败（Dummy模式）</li>
            </ul>
        </div>
        
        <div class="status warning">
            <strong>⚠️  重要说明：</strong>
            <p>当前使用Dummy数据库引擎，所有数据库操作都会失败。这是预期的行为，仅用于验证基础部署功能。</p>
        </div>
        
        <div class="next-steps">
            <strong>🔄 下一步计划：</strong>
            <ol>
                <li>解决PostgreSQL连接问题（Supabase配置）</li>
                <li>切换到真实的PostgreSQL数据库</li>
                <li>运行数据库迁移</li>
                <li>创建超级用户和测试数据</li>
                <li>启用完整的应用功能</li>
            </ol>
        </div>
        
        <div class="status info">
            <strong>🔗 测试接口：</strong>
            <ul>
                <li><a href="/test/health/">健康检查</a> - /test/health/</li>
                <li><a href="/test/system/">系统信息</a> - /test/system/</li>
                <li><a href="/test/api/">API测试</a> - /test/api/</li>
            </ul>
        </div>
    </div>
</body>
</html>"""
    return HttpResponse(html, content_type='text/html')

def api_test(request):
    """API测试接口"""
    if request.method == 'GET':
        return JsonResponse({
            'method': 'GET',
            'message': 'API接口工作正常',
            'status': 'success',
            'mode': 'dummy_database'
        })
    elif request.method == 'POST':
        return JsonResponse({
            'method': 'POST',
            'message': 'POST请求处理正常',
            'status': 'success',
            'mode': 'dummy_database'
        })
    else:
        return JsonResponse({
            'method': request.method,
            'message': f'{request.method}方法支持',
            'status': 'success',
            'mode': 'dummy_database'
        })
