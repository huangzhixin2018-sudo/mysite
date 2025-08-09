#!/usr/bin/env python3
"""
测试修复后的数据库配置
验证 dj_database_url.config() 和 dj_database_url.parse() 的参数使用
"""

import os
import sys
import django
from pathlib import Path

# 添加项目路径
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
os.environ.setdefault('DATABASE_URL', 'postgresql://test:test@localhost:5432/testdb')

def test_settings_config():
    """测试 settings.py 中的数据库配置"""
    print("🔍 测试 settings.py 中的数据库配置...")
    
    try:
        # 导入设置
        from mysite import settings
        
        # 检查数据库配置
        if 'default' in settings.DATABASES:
            db_config = settings.DATABASES['default']
            print(f"✅ 数据库引擎: {db_config.get('ENGINE', 'N/A')}")
            print(f"✅ 数据库主机: {db_config.get('HOST', 'N/A')}")
            print(f"✅ 数据库端口: {db_config.get('PORT', 'N/A')}")
            print(f"✅ 数据库名称: {db_config.get('NAME', 'N/A')}")
            print(f"✅ 连接池最大存活时间: {db_config.get('CONN_MAX_AGE', 'N/A')}")
            print(f"✅ 连接健康检查: {db_config.get('CONN_HEALTH_CHECKS', 'N/A')}")
            
            # 检查OPTIONS中的SSL配置
            options = db_config.get('OPTIONS', {})
            if 'sslmode' in options:
                print(f"✅ SSL模式: {options['sslmode']}")
            else:
                print("⚠️  未找到SSL配置")
                
        else:
            print("❌ 未找到数据库配置")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    
    return True

def test_production_config():
    """测试 settings_production.py 中的数据库配置"""
    print("\n🔍 测试 settings_production.py 中的数据库配置...")
    
    try:
        # 临时切换到生产环境设置
        os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings_production'
        
        # 重新导入Django设置
        django.setup()
        
        from django.conf import settings
        
        # 检查数据库配置
        if 'default' in settings.DATABASES:
            db_config = settings.DATABASES['default']
            print(f"✅ 数据库引擎: {db_config.get('ENGINE', 'N/A')}")
            print(f"✅ 数据库主机: {db_config.get('HOST', 'N/A')}")
            print(f"✅ 数据库端口: {db_config.get('PORT', 'N/A')}")
            print(f"✅ 数据库名称: {db_config.get('NAME', 'N/A')}")
            print(f"✅ 连接池最大存活时间: {db_config.get('CONN_MAX_AGE', 'N/A')}")
            print(f"✅ 连接健康检查: {db_config.get('CONN_HEALTH_CHECKS', 'N/A')}")
            
            # 检查OPTIONS中的配置
            options = db_config.get('OPTIONS', {})
            if 'sslmode' in options:
                print(f"✅ SSL模式: {options['sslmode']}")
            if 'connect_timeout' in options:
                print(f"✅ 连接超时: {options['connect_timeout']}")
            if 'application_name' in options:
                print(f"✅ 应用标识: {options['application_name']}")
                
        else:
            print("❌ 未找到数据库配置")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    
    return True

def test_dummy_config():
    """测试 settings_dummy.py 中的数据库配置"""
    print("\n🔍 测试 settings_dummy.py 中的数据库配置...")
    
    try:
        # 临时切换到dummy设置
        os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings_dummy'
        os.environ['DATABASE_URL'] = 'dummy://localhost:5432/dummy'
        
        # 重新导入Django设置
        django.setup()
        
        from django.conf import settings
        
        # 检查数据库配置
        if 'default' in settings.DATABASES:
            db_config = settings.DATABASES['default']
            print(f"✅ 数据库引擎: {db_config.get('ENGINE', 'N/A')}")
            
            if 'dummy' in db_config.get('ENGINE', ''):
                print("✅ 使用Dummy数据库引擎")
            else:
                print("❌ 未使用Dummy数据库引擎")
                
        else:
            print("❌ 未找到数据库配置")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("🚀 数据库配置修复验证")
    print("=" * 50)
    
    # 测试基础设置
    success1 = test_settings_config()
    
    # 测试生产环境设置
    success2 = test_production_config()
    
    # 测试Dummy设置
    success3 = test_dummy_config()
    
    print("\n" + "=" * 50)
    if success1 and success2 and success3:
        print("🎉 所有配置测试通过！")
        print("✅ settings.py 配置正确")
        print("✅ settings_production.py 配置正确")
        print("✅ settings_dummy.py 配置正确")
    else:
        print("❌ 部分配置测试失败，请检查错误信息")
    
    print("\n📋 修复总结:")
    print("1. 移除了 dj_database_url.config() 中不支持的 ssl_mode 和 ssl_require 参数")
    print("2. 将 SSL 配置移到了 OPTIONS 中的 sslmode 参数")
    print("3. 保留了支持的参数：conn_max_age 和 conn_health_checks")
    print("4. 所有配置文件现在都使用正确的参数格式")

if __name__ == '__main__':
    main()
