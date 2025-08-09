#!/usr/bin/env python3
"""
测试PostgreSQL数据库连接
"""
import os
import sys
import django
from pathlib import Path

# 添加项目根目录到Python路径
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection
from django.conf import settings

def test_database_connection():
    """测试数据库连接"""
    try:
        # 获取数据库配置信息
        db_config = settings.DATABASES['default']
        print("🔍 当前数据库配置:")
        print(f"   引擎: {db_config.get('ENGINE', 'N/A')}")
        print(f"   主机: {db_config.get('HOST', 'N/A')}")
        print(f"   端口: {db_config.get('PORT', 'N/A')}")
        print(f"   数据库: {db_config.get('NAME', 'N/A')}")
        print(f"   用户: {db_config.get('USER', 'N/A')}")
        
        # 测试连接
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ 数据库连接成功!")
            print(f"   PostgreSQL版本: {version[0]}")
            
            # 测试查询
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
    try:
        from Pythonfun.models import Category, Article
        
        # 获取分类数量
        category_count = Category.objects.count()
        print(f"📊 分类数量: {category_count}")
        
        # 获取文章数量
        article_count = Article.objects.count()
        print(f"📊 文章数量: {article_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Django模型测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始测试PostgreSQL数据库连接...")
    print("=" * 50)
    
    # 测试数据库连接
    if test_database_connection():
        print("\n" + "=" * 50)
        print("🎯 数据库连接测试完成，开始测试Django模型...")
        
        # 测试Django模型
        test_django_models()
    
    print("\n" + "=" * 50)
    print("🏁 测试完成!")
