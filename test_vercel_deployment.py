#!/usr/bin/env python3
"""
测试Vercel部署配置的脚本
"""

import os
import sys
from pathlib import Path

def test_vercel_files():
    """测试Vercel相关文件"""
    print("🔍 检查Vercel部署文件...")
    
    # 检查入口点文件
    entry_points = [
        "vercel_app/vercel_main.py",
        "vercel_app/main.py", 
        "vercel_app/simple_main.py"
    ]
    
    for entry_point in entry_points:
        if os.path.exists(entry_point):
            print(f"✅ {entry_point}: 存在")
        else:
            print(f"❌ {entry_point}: 不存在")
    
    # 检查vercel.json
    if os.path.exists("vercel.json"):
        print("✅ vercel.json: 存在")
    else:
        print("❌ vercel.json: 不存在")
    
    print()

def test_vercel_main():
    """测试vercel_main.py"""
    print("🔍 检查vercel_main.py...")
    
    try:
        # 尝试导入
        sys.path.insert(0, 'vercel_app')
        from vercel_main import handler
        
        print("✅ 导入成功")
        print("✅ handler类存在")
        
        # 检查类方法
        methods = ['do_GET', 'get_welcome_page', 'get_health_page']
        for method in methods:
            if hasattr(handler, method):
                print(f"✅ {method} 方法存在")
            else:
                print(f"❌ {method} 方法不存在")
                
    except Exception as e:
        print(f"❌ 导入失败: {e}")
    
    print()

def test_vercel_config():
    """测试vercel.json配置"""
    print("🔍 检查vercel.json配置...")
    
    try:
        import json
        with open("vercel.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # 检查必要字段
        if "builds" in config:
            print("✅ builds 配置存在")
            for build in config["builds"]:
                print(f"  - src: {build.get('src', 'N/A')}")
                print(f"  - use: {build.get('use', 'N/A')}")
        else:
            print("❌ builds 配置缺失")
        
        if "routes" in config:
            print("✅ routes 配置存在")
            for route in config["routes"]:
                print(f"  - src: {route.get('src', 'N/A')}")
                print(f"  - dest: {route.get('dest', 'N/A')}")
        else:
            print("❌ routes 配置缺失")
            
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
    
    print()

def test_django_dependency():
    """测试Django依赖"""
    print("🔍 检查Django依赖...")
    
    try:
        # 检查是否有Django相关的导入
        with open("vercel_app/vercel_main.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        if "django" in content.lower():
            print("❌ 仍然包含Django依赖")
        else:
            print("✅ 无Django依赖")
            
        if "import django" in content:
            print("❌ 包含Django导入")
        else:
            print("✅ 无Django导入")
            
    except Exception as e:
        print(f"❌ 依赖检查失败: {e}")
    
    print()

def main():
    """主函数"""
    print("🚀 开始测试Vercel部署配置...\n")
    
    test_vercel_files()
    test_vercel_main()
    test_vercel_config()
    test_django_dependency()
    
    print("🎯 测试完成！")
    print("📝 如果所有检查都通过，可以部署到Vercel了。")

if __name__ == "__main__":
    main()
