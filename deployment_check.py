#!/usr/bin/env python
"""
部署前最终检查脚本
确保项目可以成功部署到Vercel
"""

import os
import sys
from pathlib import Path

def check_project_structure():
    """检查项目结构"""
    print("📁 检查项目结构...")
    
    required_files = [
        'vercel.json',
        'requirements-vercel.txt',
        'mysite/wsgi.py',
        'mysite/settings.py',
        'manage.py'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 文件不存在")
            return False
    
    return True

def check_wsgi_config():
    """检查WSGI配置"""
    print("\n🔧 检查WSGI配置...")
    
    try:
        with open('mysite/wsgi.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'app = get_wsgi_application()' in content:
            print("✅ WSGI应用变量正确配置")
        else:
            print("❌ WSGI应用变量配置错误")
            return False
            
        if 'DJANGO_SETTINGS_MODULE' in content:
            print("✅ Django设置模块正确配置")
        else:
            print("❌ Django设置模块配置错误")
            return False
            
    except Exception as e:
        print(f"❌ 读取WSGI文件失败: {e}")
        return False
    
    return True

def check_settings_config():
    """检查Django设置配置"""
    print("\n⚙️ 检查Django设置配置...")
    
    try:
        with open('mysite/settings.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'import dj_database_url' in content:
            print("✅ dj-database-url导入正确")
        else:
            print("❌ dj-database-url导入缺失")
            return False
            
        if 'from decouple import config' in content:
            print("✅ python-decouple导入正确")
        else:
            print("❌ python-decouple导入缺失")
            return False
            
        if 'WSGI_APPLICATION = \'mysite.wsgi.app\'' in content:
            print("✅ WSGI应用路径正确")
        else:
            print("❌ WSGI应用路径错误")
            return False
            
    except Exception as e:
        print(f"❌ 读取设置文件失败: {e}")
        return False
    
    return True

def check_vercel_config():
    """检查Vercel配置"""
    print("\n🚀 检查Vercel配置...")
    
    try:
        with open('vercel.json', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '"src": "mysite/wsgi.py"' in content:
            print("✅ WSGI路径配置正确")
        else:
            print("❌ WSGI路径配置错误")
            return False
            
        if '"use": "@vercel/python"' in content:
            print("✅ Python运行时配置正确")
        else:
            print("❌ Python运行时配置错误")
            return False
            
        # 检查是否使用生产环境配置
        if '"DJANGO_SETTINGS_MODULE": "mysite.settings_production"' in content:
            print("✅ Django生产环境设置模块配置正确")
        elif '"DJANGO_SETTINGS_MODULE": "mysite.settings"' in content:
            print("✅ Django设置模块配置正确")
        else:
            print("❌ Django设置模块配置错误")
            return False
            
    except Exception as e:
        print(f"❌ 读取Vercel配置失败: {e}")
        return False
    
    return True

def check_dependencies():
    """检查依赖包"""
    print("\n📦 检查依赖包...")
    
    try:
        import django
        print(f"✅ Django: {django.get_version()}")
    except ImportError as e:
        print(f"❌ Django: {e}")
        return False
    
    try:
        import decouple
        print("✅ python-decouple")
    except ImportError as e:
        print(f"❌ python-decouple: {e}")
        return False
    
    try:
        import dj_database_url
        print("✅ dj-database-url")
    except ImportError as e:
        print(f"❌ dj-database-url: {e}")
        return False
    
    try:
        import psycopg2
        print("✅ psycopg2")
    except ImportError as e:
        print(f"❌ psycopg2: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("🚀 开始部署前最终检查...\n")
    
    checks = [
        check_project_structure,
        check_wsgi_config,
        check_settings_config,
        check_vercel_config,
        check_dependencies
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
            break
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 所有检查通过！项目可以成功部署到Vercel！")
        print("\n📋 部署步骤：")
        print("1. 在Vercel Dashboard中设置环境变量DATABASE_URL")
        print("2. 运行: vercel --prod")
        print("3. 部署完成后运行: python create_postgres_tables.py")
    else:
        print("❌ 部分检查失败，请修复问题后重试")
        print("\n💡 建议运行: python test_dependencies.py")
    
    print("="*50)

if __name__ == '__main__':
    main()
