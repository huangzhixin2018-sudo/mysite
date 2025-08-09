#!/usr/bin/env python3
"""
简化的测试脚本 - 避免Unicode编码问题
"""
import os
import sys
from pathlib import Path

def test_basic_functionality():
    """测试基本功能"""
    print("=== 基本功能测试 ===")
    
    # 检查环境变量
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        print("[OK] DATABASE_URL 已设置")
        safe_url = database_url.replace('huangzhixin2025', '***')
        print(f"    连接字符串: {safe_url}")
    else:
        print("[ERROR] DATABASE_URL 未设置")
        return False
    
    # 检查Django配置
    try:
        BASE_DIR = Path(__file__).resolve().parent
        sys.path.append(str(BASE_DIR))
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
        
        import django
        django.setup()
        
        from django.conf import settings
        
        print("[OK] Django环境设置成功")
        
        # 检查数据库配置
        db_config = settings.DATABASES['default']
        print(f"    数据库引擎: {db_config.get('ENGINE', 'N/A')}")
        print(f"    数据库主机: {db_config.get('HOST', 'N/A')}")
        print(f"    数据库端口: {db_config.get('PORT', 'N/A')}")
        print(f"    数据库名称: {db_config.get('NAME', 'N/A')}")
        print(f"    数据库用户: {db_config.get('USER', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Django配置检查失败: {e}")
        return False

def test_database_connection():
    """测试数据库连接"""
    print("\n=== 数据库连接测试 ===")
    
    try:
        from django.db import connection
        
        # 测试连接
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print("[OK] 数据库连接成功!")
            print(f"    PostgreSQL版本: {version[0]}")
            
            # 测试基本查询
            cursor.execute("SELECT current_database(), current_user, inet_server_addr();")
            db_info = cursor.fetchone()
            print(f"    当前数据库: {db_info[0]}")
            print(f"    当前用户: {db_info[1]}")
            print(f"    服务器地址: {db_info[2]}")
            
        return True
        
    except Exception as e:
        print(f"[ERROR] 数据库连接失败: {e}")
        return False

def test_django_models():
    """测试Django模型"""
    print("\n=== Django模型测试 ===")
    
    try:
        from Pythonfun.models import Category, Article
        
        # 获取分类数量
        category_count = Category.objects.count()
        print(f"[OK] 分类模型正常: {category_count} 个分类")
        
        # 获取文章数量
        article_count = Article.objects.count()
        print(f"[OK] 文章模型正常: {article_count} 篇文章")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Django模型测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试...")
    print("=" * 50)
    
    # 测试基本功能
    basic_ok = test_basic_functionality()
    
    if basic_ok:
        # 测试数据库连接
        db_ok = test_database_connection()
        
        if db_ok:
            # 测试Django模型
            models_ok = test_django_models()
        else:
            models_ok = False
    else:
        db_ok = False
        models_ok = False
    
    # 测试结果总结
    print("\n" + "=" * 50)
    print("测试结果总结")
    print("=" * 50)
    print(f"基本功能: {'[OK] 通过' if basic_ok else '[ERROR] 失败'}")
    print(f"数据库连接: {'[OK] 通过' if db_ok else '[ERROR] 失败'}")
    print(f"Django模型: {'[OK] 通过' if models_ok else '[ERROR] 失败'}")
    
    if all([basic_ok, db_ok, models_ok]):
        print("\n[SUCCESS] 所有测试通过！系统准备就绪，可以上线！")
        return True
    else:
        print("\n[WARNING] 部分测试失败，请检查配置后重试。")
        return False

if __name__ == "__main__":
    main()
