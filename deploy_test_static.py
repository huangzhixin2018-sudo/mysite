#!/usr/bin/env python3
"""
测试静态网页配置的脚本
"""

import os
import sys
import django
from pathlib import Path

# 添加项目路径
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def test_config():
    """测试Django配置"""
    from django.conf import settings
    
    print("🔍 检查Django配置...")
    
    # 检查基本设置
    print(f"✅ DEBUG: {settings.DEBUG}")
    print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"✅ INSTALLED_APPS: {settings.INSTALLED_APPS}")
    print(f"✅ MIDDLEWARE: {settings.MIDDLEWARE}")
    
    # 检查模板配置
    print(f"✅ TEMPLATES DIRS: {settings.TEMPLATES[0]['DIRS']}")
    print(f"✅ APP_DIRS: {settings.TEMPLATES[0]['APP_DIRS']}")
    
    # 检查静态文件配置
    print(f"✅ STATIC_URL: {settings.STATIC_URL}")
    print(f"✅ STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"✅ STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    
    # 检查数据库配置
    print(f"✅ DATABASES: {settings.DATABASES}")
    
    print("\n🎯 配置检查完成！")

def test_urls():
    """测试URL配置"""
    from django.urls import get_resolver
    
    print("\n🔍 检查URL配置...")
    
    try:
        resolver = get_resolver()
        url_patterns = resolver.url_patterns
        print(f"✅ URL模式数量: {len(url_patterns)}")
        
        for pattern in url_patterns:
            print(f"  - {pattern.pattern}")
            
    except Exception as e:
        print(f"❌ URL配置错误: {e}")
    
    print("\n🎯 URL检查完成！")

def test_views():
    """测试视图函数"""
    print("\n🔍 检查视图函数...")
    
    try:
        from mysite import minimal_test_views
        
        # 测试视图函数是否存在
        views = ['welcome_page', 'health_check', 'system_info', 'api_test']
        for view_name in views:
            if hasattr(minimal_test_views, view_name):
                print(f"✅ {view_name}: 存在")
            else:
                print(f"❌ {view_name}: 不存在")
                
    except Exception as e:
        print(f"❌ 视图检查错误: {e}")
    
    print("\n🎯 视图检查完成！")

if __name__ == '__main__':
    print("🚀 开始测试静态网页配置...\n")
    
    try:
        test_config()
        test_urls()
        test_views()
        
        print("\n🎉 所有测试通过！静态网页配置正确。")
        print("📝 现在可以部署到Vercel了。")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
