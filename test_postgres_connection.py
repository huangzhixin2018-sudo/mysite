#!/usr/bin/env python3
"""
PostgreSQL数据库连接测试脚本
用于验证数据库配置是否正确
"""

import os
import sys
import django
from django.conf import settings
from django.db import connection
from django.core.management import execute_from_command_line

def test_database_connection():
    """测试数据库连接"""
    print("🔍 开始测试PostgreSQL数据库连接...")
    
    try:
        # 设置Django环境
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
        django.setup()
        
        # 检查数据库配置
        db_config = settings.DATABASES['default']
        print(f"📊 数据库配置信息:")
        print(f"   引擎: {db_config.get('ENGINE', 'N/A')}")
        print(f"   主机: {db_config.get('HOST', 'N/A')}")
        print(f"   端口: {db_config.get('PORT', 'N/A')}")
        print(f"   数据库: {db_config.get('NAME', 'N/A')}")
        print(f"   用户: {db_config.get('USER', 'N/A')}")
        print(f"   SSL模式: {db_config.get('OPTIONS', {}).get('sslmode', 'N/A')}")
        
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
        print(f"❌ 数据库连接失败: {str(e)}")
        print(f"   错误类型: {type(e).__name__}")
        return False

def test_django_models():
    """测试Django模型"""
    print("\n🔍 测试Django模型...")
    
    try:
        from Pythonfun.models import Category, Article
        
        # 测试模型导入
        print(f"✅ 模型导入成功:")
        print(f"   Category: {Category}")
        print(f"   Article: {Article}")
        
        # 测试数据库表
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
            print(f"📋 数据库表列表:")
            for table in tables:
                print(f"   - {table[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ 模型测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 PostgreSQL数据库连接测试工具")
    print("=" * 50)
    
    # 检查环境变量
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        print(f"📝 检测到DATABASE_URL环境变量: {database_url[:50]}...")
    else:
        print("⚠️  未检测到DATABASE_URL环境变量")
    
    # 测试数据库连接
    connection_ok = test_database_connection()
    
    if connection_ok:
        # 测试Django模型
        models_ok = test_django_models()
        
        print("\n" + "=" * 50)
        if models_ok:
            print("🎉 所有测试通过! 数据库配置正确.")
        else:
            print("⚠️  数据库连接正常，但模型测试失败.")
    else:
        print("\n" + "=" * 50)
        print("❌ 数据库连接测试失败，请检查配置.")
    
    print("\n💡 如果遇到问题，请检查:")
    print("   1. DATABASE_URL环境变量是否正确")
    print("   2. 数据库服务器是否可访问")
    print("   3. 防火墙和安全组设置")
    print("   4. 数据库用户权限")

if __name__ == '__main__':
    main()
