#!/usr/bin/env python3
"""
部署测试脚本 - 检查所有必要的组件
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_dependencies():
    """检查Python依赖"""
    print("🐍 Python依赖检查")
    print("=" * 50)
    
    required_packages = [
        'django',
        'psycopg2',
        'dj-database-url',
        'python-decouple'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install " + " ".join(missing_packages))
        return False
    
    return True

def check_django_configuration():
    """检查Django配置"""
    print("\n⚙️ Django配置检查")
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
        
        print("✅ Django环境设置成功")
        print(f"   项目名称: {settings.SETTINGS_MODULE}")
        print(f"   调试模式: {settings.DEBUG}")
        print(f"   允许主机: {settings.ALLOWED_HOSTS}")
        
        # 检查数据库配置
        db_config = settings.DATABASES['default']
        print(f"   数据库引擎: {db_config.get('ENGINE', 'N/A')}")
        print(f"   数据库主机: {db_config.get('HOST', 'N/A')}")
        print(f"   数据库端口: {db_config.get('PORT', 'N/A')}")
        print(f"   数据库名称: {db_config.get('NAME', 'N/A')}")
        print(f"   数据库用户: {db_config.get('USER', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Django配置检查失败: {e}")
        return False

def check_environment_variables():
    """检查环境变量"""
    print("\n🔧 环境变量检查")
    print("=" * 50)
    
    required_vars = ['DATABASE_URL']
    optional_vars = ['SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS']
    
    all_good = True
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var} - 已设置")
            if var == 'DATABASE_URL':
                # 隐藏密码显示
                safe_value = value.replace('huangzhixin2025', '***')
                print(f"   值: {safe_value}")
        else:
            print(f"❌ {var} - 未设置")
            all_good = False
    
    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var} - 已设置")
        else:
            print(f"⚠️ {var} - 未设置（可选）")
    
    return all_good

def check_static_files():
    """检查静态文件"""
    print("\n📁 静态文件检查")
    print("=" * 50)
    
    static_dir = Path("static")
    staticfiles_dir = Path("staticfiles")
    templates_dir = Path("templates")
    
    if static_dir.exists():
        print(f"✅ static/ 目录存在")
    else:
        print(f"❌ static/ 目录不存在")
    
    if staticfiles_dir.exists():
        print(f"✅ staticfiles/ 目录存在")
    else:
        print(f"⚠️ staticfiles/ 目录不存在（部署时会创建）")
    
    if templates_dir.exists():
        print(f"✅ templates/ 目录存在")
        # 检查关键模板
        key_templates = [
            "admin/登录.html",
            "admin/分类管理.html", 
            "admin/教程管理.html",
            "front/index.html"
        ]
        for template in key_templates:
            if (templates_dir / template).exists():
                print(f"   ✅ {template}")
            else:
                print(f"   ❌ {template}")
    else:
        print(f"❌ templates/ 目录不存在")
    
    return True

def check_database_migration():
    """检查数据库迁移状态"""
    print("\n🗄️ 数据库迁移检查")
    print("=" * 50)
    
    try:
        # 添加项目根目录到Python路径
        BASE_DIR = Path(__file__).resolve().parent
        sys.path.append(str(BASE_DIR))
        
        # 设置Django环境
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
        
        import django
        django.setup()
        
        from django.core.management import execute_from_command_line
        
        # 检查迁移状态
        result = subprocess.run([
            sys.executable, 'manage.py', 'showmigrations'
        ], capture_output=True, text=True, cwd=BASE_DIR)
        
        if result.returncode == 0:
            print("✅ 迁移检查成功")
            print("   迁移状态:")
            for line in result.stdout.split('\n'):
                if line.strip() and ('[X]' in line or '[ ]' in line):
                    print(f"   {line}")
        else:
            print(f"❌ 迁移检查失败: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 数据库迁移检查失败: {e}")
        return False

def check_vercel_configuration():
    """检查Vercel配置"""
    print("\n🚀 Vercel配置检查")
    print("=" * 50)
    
    vercel_json = Path("vercel.json")
    vercel_env = Path("vercel.env")
    
    if vercel_json.exists():
        print("✅ vercel.json 存在")
    else:
        print("❌ vercel.json 不存在")
    
    if vercel_env.exists():
        print("✅ vercel.env 存在")
    else:
        print("❌ vercel.env 不存在")
    
    # 检查requirements文件
    requirements_files = ["requirements.txt", "requirements-vercel.txt"]
    for req_file in requirements_files:
        if Path(req_file).exists():
            print(f"✅ {req_file} 存在")
        else:
            print(f"❌ {req_file} 不存在")
    
    return True

def run_django_health_check():
    """运行Django健康检查"""
    print("\n🏥 Django健康检查")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'check', '--deploy'
        ], capture_output=True, text=True, cwd=Path(__file__).resolve().parent)
        
        if result.returncode == 0:
            print("✅ Django健康检查通过")
            print("   部署检查结果:")
            for line in result.stdout.split('\n'):
                if line.strip() and not line.startswith('System check'):
                    print(f"   {line}")
        else:
            print(f"❌ Django健康检查失败: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Django健康检查异常: {e}")
        return False

def main():
    """主检查函数"""
    print("🚀 开始部署前检查...")
    print("=" * 60)
    
    # 显示系统信息
    print(f"💻 系统信息: {platform.system()} {platform.release()}")
    print(f"🐍 Python版本: {platform.python_version()}")
    print(f"📁 工作目录: {os.getcwd()}")
    print("=" * 60)
    
    # 执行各项检查
    checks = [
        ("Python依赖", check_python_dependencies),
        ("环境变量", check_environment_variables),
        ("Django配置", check_django_configuration),
        ("静态文件", check_static_files),
        ("Vercel配置", check_vercel_configuration),
        ("数据库迁移", check_database_migration),
        ("Django健康检查", run_django_health_check),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ {check_name} 检查异常: {e}")
            results[check_name] = False
    
    # 检查结果总结
    print("\n" + "=" * 60)
    print("📋 检查结果总结")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for check_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{check_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项检查通过")
    
    if passed == total:
        print("\n🎉 所有检查通过！系统准备就绪，可以部署上线！")
        print("\n📝 部署建议:")
        print("1. 确保Vercel环境变量已正确设置")
        print("2. 运行 'vercel --prod' 进行生产部署")
        print("3. 部署后验证网站功能")
        return True
    else:
        print(f"\n⚠️ 有 {total - passed} 项检查失败，请修复后重试。")
        print("\n🔧 修复建议:")
        if not results.get("环境变量", True):
            print("- 检查环境变量设置")
        if not results.get("Django配置", True):
            print("- 检查Django配置文件")
        if not results.get("数据库迁移", True):
            print("- 运行数据库迁移")
        return False

if __name__ == "__main__":
    main()
