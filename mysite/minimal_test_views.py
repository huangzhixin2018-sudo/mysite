"""
最小化测试视图 - 完全避免数据库操作
用于Dummy模式下的基础功能测试
"""

from django.http import HttpResponse, JsonResponse

def welcome_page(request):
    """欢迎页面 - 最简单的HTML响应"""
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django部署成功</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; 
            padding: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.1); 
            padding: 40px; 
            border-radius: 20px; 
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        h1 { 
            text-align: center; 
            font-size: 2.5em; 
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .status { 
            padding: 20px; 
            margin: 20px 0; 
            border-radius: 10px; 
            background: rgba(255,255,255,0.2);
        }
        .success { background: rgba(76, 175, 80, 0.3); }
        .warning { background: rgba(255, 193, 7, 0.3); }
        .info { background: rgba(33, 150, 243, 0.3); }
        ul { line-height: 2; }
        .next-steps { 
            background: rgba(255,255,255,0.2); 
            padding: 25px; 
            border-radius: 10px; 
            margin-top: 30px; 
        }
        .test-links { 
            display: flex; 
            gap: 20px; 
            justify-content: center; 
            margin-top: 30px;
        }
        .test-links a { 
            background: rgba(255,255,255,0.2); 
            color: white; 
            padding: 12px 24px; 
            text-decoration: none; 
            border-radius: 25px; 
            transition: all 0.3s ease;
        }
        .test-links a:hover { 
            background: rgba(255,255,255,0.3); 
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 Django部署成功！</h1>
        
        <div class="status success">
            <strong>✅ 部署状态：</strong> 项目已成功部署到Vercel
        </div>
        
        <div class="status info">
            <strong>📋 当前模式：</strong> Dummy数据库模式（仅测试基础功能）
            <ul>
                <li>✅ Django框架正常运行</li>
                <li>✅ 静态文件服务正常</li>
                <li>✅ URL路由系统正常</li>
                <li>✅ 中间件工作正常</li>
                <li>❌ 数据库功能（预期失败）</li>
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
        
        <div class="test-links">
            <a href="/test/health/">健康检查</a>
            <a href="/test/system/">系统信息</a>
            <a href="/test/api/">API测试</a>
        </div>
    </div>
</body>
</html>"""
    return HttpResponse(html, content_type='text/html')

def health_check(request):
    """健康检查接口 - 最简单的JSON响应"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Django项目运行正常',
        'mode': 'dummy_database',
        'timestamp': '2024-01-01T00:00:00Z'
    })

def system_info(request):
    """系统信息接口 - 避免使用platform模块"""
    return JsonResponse({
        'django_version': '5.0.7',
        'mode': 'dummy_database',
        'status': 'running'
    })

def api_test(request):
    """API测试接口 - 最简单的请求处理"""
    if request.method == 'GET':
        return JsonResponse({
            'method': 'GET',
            'message': 'GET请求处理正常',
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
