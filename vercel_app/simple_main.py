"""
简单的Vercel Python运行时入口点 - 纯HTML响应
"""

def handler(request, context):
    """Vercel Python运行时入口点"""
    try:
        path = request.get('path', '/')
        
        # 简单的路由分发
        if path == '/':
            html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vercel部署成功</title>
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
        .info { background: rgba(33, 150, 243, 0.3); }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 Vercel部署成功！</h1>
        
        <div class="status success">
            <strong>✅ 部署状态：</strong> 项目已成功部署到Vercel
        </div>
        
        <div class="status info">
            <strong>📋 当前模式：</strong> 纯Python运行时
            <ul>
                <li>✅ Vercel Python运行时正常</li>
                <li>✅ 路由系统正常</li>
                <li>✅ HTML响应正常</li>
                <li>✅ 无Django依赖</li>
            </ul>
        </div>
        
        <div class="status info">
            <strong>🔗 测试链接：</strong>
            <ul>
                <li><a href="/test/health/" style="color: white;">健康检查</a></li>
                <li><a href="/test/system/" style="color: white;">系统信息</a></li>
                <li><a href="/test/api/" style="color: white;">API测试</a></li>
            </ul>
        </div>
    </div>
</body>
</html>"""
            
        elif path == '/test/health/':
            html = """<!DOCTYPE html>
<html><body><h1>健康检查</h1><p>状态：正常</p></body></html>"""
            
        elif path == '/test/system/':
            html = """<!DOCTYPE html>
<html><body><h1>系统信息</h1><p>运行时：Python 3.9</p><p>平台：Vercel</p></body></html>"""
            
        elif path == '/test/api/':
            html = """<!DOCTYPE html>
<html><body><h1>API测试</h1><p>状态：成功</p><p>方法：GET</p></body></html>"""
            
        else:
            html = """<!DOCTYPE html>
<html><body><h1>404 - 页面未找到</h1><p>请求的路径不存在</p></body></html>"""
        
        return {
            'statusCode': 200,
            'body': html,
            'headers': {'Content-Type': 'text/html; charset=utf-8'}
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'<h1>服务器错误</h1><p>{str(e)}</p>',
            'headers': {'Content-Type': 'text/html; charset=utf-8'}
        }

# Vercel Python运行时要求
app = handler
