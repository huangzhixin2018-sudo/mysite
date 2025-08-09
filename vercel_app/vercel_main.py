"""
Vercel Python运行时标准入口点
"""

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理GET请求"""
        try:
            # 解析路径
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            # 设置响应头
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # 路由分发
            if path == '/':
                html = self.get_welcome_page()
            elif path == '/test/health/':
                html = self.get_health_page()
            elif path == '/test/system/':
                html = self.get_system_page()
            elif path == '/test/api/':
                html = self.get_api_page()
            elif path in ['/favicon.ico', '/favicon.png']:
                html = self.get_favicon_response()
            else:
                html = self.get_404_page()
            
            # 返回HTML
            self.wfile.write(html.encode('utf-8'))
            
        except Exception as e:
            # 错误处理
            self.send_response(500)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            error_html = f'<h1>服务器错误</h1><p>{str(e)}</p>'
            self.wfile.write(error_html.encode('utf-8'))
    
    def get_welcome_page(self):
        """欢迎页面"""
        return """<!DOCTYPE html>
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
    
    def get_health_page(self):
        """健康检查页面"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>健康检查</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; }
        .status { color: green; font-size: 24px; }
    </style>
</head>
<body>
    <h1>健康检查</h1>
    <p class="status">✅ 状态：正常</p>
    <p>Vercel Python运行时工作正常</p>
    <a href="/">返回首页</a>
</body>
</html>"""
    
    def get_system_page(self):
        """系统信息页面"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>系统信息</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; }
        .info { background: #f0f0f0; padding: 20px; border-radius: 10px; }
    </style>
</head>
<body>
    <h1>系统信息</h1>
    <div class="info">
        <p><strong>运行时：</strong> Python 3.9</p>
        <p><strong>平台：</strong> Vercel</p>
        <p><strong>架构：</strong> 无服务器函数</p>
    </div>
    <a href="/">返回首页</a>
</body>
</html>"""
    
    def get_api_page(self):
        """API测试页面"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>API测试</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; }
        .success { color: green; font-size: 20px; }
    </style>
</head>
<body>
    <h1>API测试</h1>
    <p class="success">✅ 状态：成功</p>
    <p><strong>方法：</strong> GET</p>
    <p><strong>响应：</strong> HTML</p>
    <a href="/">返回首页</a>
</body>
</html>"""
    
    def get_favicon_response(self):
        """favicon响应"""
        return """<!DOCTYPE html>
<html>
<head>
    <title>Favicon</title>
</head>
<body>
    <p>Favicon请求已处理</p>
</body>
</html>"""
    
    def get_404_page(self):
        """404页面"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>页面未找到</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; text-align: center; }
        .error { color: red; font-size: 24px; }
    </style>
</head>
<body>
    <h1 class="error">404 - 页面未找到</h1>
    <p>请求的路径不存在</p>
    <a href="/">返回首页</a>
</body>
</html>"""
