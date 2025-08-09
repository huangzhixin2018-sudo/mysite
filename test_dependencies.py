#!/usr/bin/env python
"""
测试依赖包安装脚本
确保所有必要的包都已正确安装
"""

def test_dependencies():
    """测试所有必要的依赖包"""
    print("🔍 测试依赖包安装状态...")
    
    # 测试基础包
    try:
        import django
        print(f"✅ Django: {django.get_version()}")
    except ImportError as e:
        print(f"❌ Django: {e}")
        return False
    
    try:
        import decouple
        print("✅ python-decouple: 已安装")
    except ImportError as e:
        print(f"❌ python-decouple: {e}")
        return False
    
    try:
        import dj_database_url
        print("✅ dj-database-url: 已安装")
    except ImportError as e:
        print(f"❌ dj-database-url: {e}")
        return False
    
    try:
        import psycopg2
        print("✅ psycopg2: 已安装")
    except ImportError as e:
        print(f"❌ psycopg2: {e}")
        return False
    
    try:
        import PIL
        print("✅ Pillow: 已安装")
    except ImportError as e:
        print(f"❌ Pillow: {e}")
        return False
    
    try:
        import whitenoise
        print("✅ whitenoise: 已安装")
    except ImportError as e:
        print(f"❌ whitenoise: {e}")
        return False
    
    try:
        import corsheaders
        print("✅ django-cors-headers: 已安装")
    except ImportError as e:
        print(f"❌ django-cors-headers: {e}")
        return False
    
    try:
        import storages
        print("✅ django-storages: 已安装")
    except ImportError as e:
        print(f"❌ django-storages: {e}")
        return False
    
    print("\n🎯 所有依赖包测试完成！")
    return True

def test_database_config():
    """测试数据库配置"""
    print("\n🗄️ 测试数据库配置...")
    
    try:
        from decouple import config
        database_url = config('DATABASE_URL', default=None)
        
        if database_url:
            print(f"✅ DATABASE_URL: {database_url[:50]}...")
            
            # 测试解析
            import dj_database_url
            db_config = dj_database_url.parse(database_url)
            print(f"✅ 数据库配置解析成功: {db_config['ENGINE']}")
            
        else:
            print("ℹ️ DATABASE_URL 未设置，将使用SQLite")
            
    except Exception as e:
        print(f"❌ 数据库配置测试失败: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("🚀 开始测试项目依赖...\n")
    
    deps_ok = test_dependencies()
    db_ok = test_database_config()
    
    if deps_ok and db_ok:
        print("\n🎉 所有测试通过！项目可以正常部署。")
    else:
        print("\n⚠️ 部分测试失败，请检查依赖包安装。")
        print("💡 建议运行: pip install -r requirements-vercel.txt")
