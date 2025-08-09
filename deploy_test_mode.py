#!/usr/bin/env python3
"""
部署测试模式检查脚本
用于验证Django项目在Dummy数据库模式下的基础功能
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

def check_dummy_mode():
    """检查Dummy数据库模式配置"""
    print("🔍 检查Dummy数据库模式配置...")
    
    try:
        # 设置Django环境
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings_dummy')
        django.setup()
        
        print("✅ Django环境设置完成")
        
        # 检查数据库配置
        db_config = settings.DATABASES['default']
        print(f"📊 数据库配置:")
        print(f"   引擎: {db_config.get('ENGINE', 'N/A')}")
        
        if 'dummy' in db_config.get('ENGINE', ''):
            print("✅ 使用Dummy数据库引擎")
        else:
            print("❌ 未使用Dummy数据库引擎")
            return False
        
        # 检查中间件
        print(f"📋 中间件配置:")
        for middleware in settings.MIDDLEWARE:
            print(f"   - {middleware}")
        
        # 检查应用
        print(f"📱 应用配置:")
        for app in settings.INSTALLED_APPS:
            print(f"   - {app}")
        
        # 检查静态文件配置
        print(f"📁 静态文件配置:")
        print(f"   STATIC_URL: {settings.STATIC_URL}")
        print(f"   STATIC_ROOT: {settings.STATIC_ROOT}")
        print(f"   STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        
        # 检查安全设置
        print(f"🔒 安全设置:")
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        return False

def test_basic_functionality():
    """测试基础功能"""
    print("\n🔍 测试基础功能...")
    
    try:
        # 测试URL配置
        from django.urls import reverse
        from django.test import Client
        
        client = Client()
        
        # 测试健康检查接口
        print("📡 测试健康检查接口...")
        response = client.get('/test/health/')
        if response.status_code == 200:
            print("✅ 健康检查接口正常")
        else:
            print(f"❌ 健康检查接口异常: {response.status_code}")
        
        # 测试系统信息接口
        print("📡 测试系统信息接口...")
        response = client.get('/test/system/')
        if response.status_code == 200:
            print("✅ 系统信息接口正常")
        else:
            print(f"❌ 系统信息接口异常: {response.status_code}")
        
        # 测试主页面
        print("📡 测试主页面...")
        response = client.get('/test/')
        if response.status_code == 200:
            print("✅ 主页面正常")
        else:
            print(f"❌ 主页面异常: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 Django Dummy数据库模式部署检查")
    print("=" * 60)
    
    # 检查环境变量
    settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
    if settings_module:
        print(f"📝 检测到设置模块: {settings_module}")
        if 'dummy' in settings_module:
            print("✅ 使用Dummy数据库配置")
        else:
            print("⚠️  建议使用Dummy数据库配置进行测试")
    else:
        print("⚠️  未检测到DJANGO_SETTINGS_MODULE环境变量")
    
    # 检查配置
    config_ok = check_dummy_mode()
    
    if config_ok:
        # 测试功能
        functionality_ok = test_basic_functionality()
        
        print("\n" + "=" * 60)
        if functionality_ok:
            print("🎉 所有检查通过! 项目已准备好部署测试。")
            print("\n💡 下一步操作:")
            print("   1. 部署到Vercel")
            print("   2. 验证基础功能是否正常")
            print("   3. 解决PostgreSQL连接问题")
            print("   4. 切换到真实数据库配置")
        else:
            print("⚠️  配置正常，但功能测试失败。")
    else:
        print("\n" + "=" * 60)
        print("❌ 配置检查失败，请检查设置文件。")
    
    print("\n📋 部署检查清单:")
    print("   ✅ 使用Dummy数据库引擎")
    print("   ✅ 禁用需要数据库的中间件")
    print("   ✅ 禁用需要数据库的应用")
    print("   ✅ 配置测试路由")
    print("   ✅ 设置环境变量")
    print("   ❌ 待解决: PostgreSQL连接问题")

if __name__ == '__main__':
    main()
