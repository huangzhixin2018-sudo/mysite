#!/usr/bin/env python3
"""
全面的连接测试脚本 - 用于上线前测试
"""
import os
import sys
import socket
import subprocess
import platform
from pathlib import Path

def test_network_connectivity():
    """测试网络连接"""
    print("🌐 网络连接测试")
    print("=" * 50)
    
    # 测试DNS解析
    host = "db.wjuaayjnetykmnyqejhi.supabase.co"
    try:
        ip = socket.gethostbyname(host)
        print(f"✅ DNS解析成功: {host} -> {ip}")
    except socket.gaierror as e:
        print(f"❌ DNS解析失败: {e}")
        return False
    
    # 测试端口连接
    port = 5432
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ 端口连接成功: {host}:{port}")
        else:
            print(f"❌ 端口连接失败: {host}:{port} (错误码: {result})")
            return False
    except Exception as e:
        print(f"❌ 端口连接测试异常: {e}")
        return False
    
    return True

def test_environment_variables():
    """测试环境变量"""
    print("\n🔧 环境变量测试")
    print("=" * 50)
    
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        print(f"✅ DATABASE_URL 已设置")
        # 隐藏密码显示
        safe_url = database_url.replace('huangzhixin2025', '***')
        print(f"   连接字符串: {safe_url}")
    else:
        print("❌ DATABASE_URL 未设置")
        return False
    
    return True

def test_django_setup():
    """测试Django设置"""
    print("\n🐍 Django设置测试")
    print("=" * 50)
    
    try:
        # 添加项目根目录到Python路径
        BASE_DIR = Path(__file__).resolve().parent
        sys.path.append(str(BASE_DIR))
        
        # 设置Django环境
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
        
        import django
        django.setup()
        
        from django.conf import settings
        from django.db import connection
        
        print("✅ Django环境设置成功")
        
        # 检查数据库配置
        db_config = settings.DATABASES['default']
        print(f"   数据库引擎: {db_config.get('ENGINE', 'N/A')}")
        print(f"   数据库主机: {db_config.get('HOST', 'N/A')}")
        print(f"   数据库端口: {db_config.get('PORT', 'N/A')}")
        print(f"   数据库名称: {db_config.get('NAME', 'N/A')}")
        print(f"   数据库用户: {db_config.get('USER', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Django设置失败: {e}")
        return False

def test_database_connection():
    """测试数据库连接"""
    print("\n🗄️ 数据库连接测试")
    print("=" * 50)
    
    try:
        from django.db import connection
        
        # 测试连接
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ 数据库连接成功!")
            print(f"   PostgreSQL版本: {version[0]}")
            
            # 测试基本查询
            cursor.execute("SELECT current_database(), current_user, inet_server_addr();")
            db_info = cursor.fetchone()
            print(f"   当前数据库: {db_info[0]}")
            print(f"   当前用户: {db_info[1]}")
            print(f"   服务器地址: {db_info[2]}")
            
        return True
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def test_django_models():
    """测试Django模型"""
    print("\n📊 Django模型测试")
    print("=" * 50)
    
    try:
        from Pythonfun.models import Category, Article
        
        # 获取分类数量
        category_count = Category.objects.count()
        print(f"✅ 分类模型正常: {category_count} 个分类")
        
        # 获取文章数量
        article_count = Article.objects.count()
        print(f"✅ 文章模型正常: {article_count} 篇文章")
        
        return True
        
    except Exception as e:
        print(f"❌ Django模型测试失败: {e}")
        return False

def test_system_info():
    """显示系统信息"""
    print("\n💻 系统信息")
    print("=" * 50)
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"Python版本: {platform.python_version()}")
    print(f"Python路径: {sys.executable}")
    print(f"当前工作目录: {os.getcwd()}")

def main():
    """主测试函数"""
    print("🚀 开始全面连接测试...")
    print("=" * 60)
    
    # 显示系统信息
    test_system_info()
    
    # 测试网络连接
    network_ok = test_network_connectivity()
    
    # 测试环境变量
    env_ok = test_environment_variables()
    
    # 测试Django设置
    django_ok = test_django_setup()
    
    # 如果前面的测试都通过，继续测试数据库
    if network_ok and env_ok and django_ok:
        db_ok = test_database_connection()
        
        if db_ok:
            models_ok = test_django_models()
        else:
            models_ok = False
    else:
        db_ok = False
        models_ok = False
    
    # 测试结果总结
    print("\n" + "=" * 60)
    print("📋 测试结果总结")
    print("=" * 60)
    print(f"网络连接: {'✅ 通过' if network_ok else '❌ 失败'}")
    print(f"环境变量: {'✅ 通过' if env_ok else '❌ 失败'}")
    print(f"Django设置: {'✅ 通过' if django_ok else '❌ 失败'}")
    print(f"数据库连接: {'✅ 通过' if db_ok else '❌ 失败'}")
    print(f"Django模型: {'✅ 通过' if models_ok else '❌ 失败'}")
    
    if all([network_ok, env_ok, django_ok, db_ok, models_ok]):
        print("\n🎉 所有测试通过！系统准备就绪，可以上线！")
        return True
    else:
        print("\n⚠️ 部分测试失败，请检查配置后重试。")
        return False

if __name__ == "__main__":
    main()
