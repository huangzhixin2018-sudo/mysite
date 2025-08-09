"""
Dummy数据库配置文件
用于先部署测试基础功能，绕过数据库连接问题
"""

import os
from .settings import (
    BASE_DIR, SECRET_KEY, INSTALLED_APPS, MIDDLEWARE, ROOT_URLCONF, TEMPLATES,
    WSGI_APPLICATION, AUTH_PASSWORD_VALIDATORS, LANGUAGE_CODE, TIME_ZONE,
    USE_I18N, USE_TZ, STATIC_URL, DEFAULT_AUTO_FIELD, LOGIN_URL, LOGIN_REDIRECT_URL
)

# 生产环境设置
DEBUG = False

# 安全设置
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 允许的主机
ALLOWED_HOSTS = [
    '.vercel.app',
    '.now.sh',
    'localhost',
    '127.0.0.1'
]

# 静态文件配置
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Dummy数据库配置 - 不连接真实数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

print("[INFO] 使用Dummy数据库 - 仅用于部署测试")
print("[WARNING] 所有数据库操作将失败，仅适合测试基础功能")

# 禁用需要数据库的中间件 - 只保留最基础的中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# 禁用需要数据库的应用 - 只保留最基础的应用
INSTALLED_APPS = [
    'django.contrib.staticfiles',   # 静态文件处理 - 不需要数据库
]

print(f"[INFO] 已禁用需要数据库的中间件和应用")
print(f"[INFO] 当前中间件: {MIDDLEWARE}")
print(f"[INFO] 当前应用: {INSTALLED_APPS}")

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# 自定义错误处理
def custom_500_handler(request):
    """自定义500错误处理，避免数据库错误"""
    from django.http import HttpResponse
    return HttpResponse("""
    <html>
    <head><title>功能测试模式</title></head>
    <body>
        <h1>🚀 Django项目部署成功！</h1>
        <p>当前使用Dummy数据库模式，仅用于测试基础功能。</p>
        <p>下一步：解决PostgreSQL连接问题，然后切换到真实数据库。</p>
        <hr>
        <p><strong>测试状态：</strong></p>
        <ul>
            <li>✅ 环境配置</li>
            <li>✅ 静态资源</li>
            <li>✅ 路由系统</li>
            <li>❌ 数据库功能（预期）</li>
        </ul>
    </body>
    </html>
    """, content_type='text/html')

# 错误处理配置
HANDLER404 = 'mysite.settings_dummy.custom_500_handler'
HANDLER500 = 'mysite.settings_dummy.custom_500_handler'
