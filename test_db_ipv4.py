#!/usr/bin/env python3
"""
强制使用IPv4测试PostgreSQL数据库连接
"""
import os
import socket
import psycopg2
from urllib.parse import urlparse

def test_ipv4_connection():
    """强制使用IPv4连接"""
    print("=== 强制IPv4连接测试 ===")
    
    # 从nslookup结果获取的IPv6地址
    ipv6_address = "2406:da18:243:740a:b3a7:c514:1fb4:7520"
    port = 5432
    
    try:
        # 尝试直接连接IPv6地址
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((ipv6_address, port))
        sock.close()
        
        if result == 0:
            print(f"[OK] 直接IPv6连接成功: {ipv6_address}:{port}")
            return ipv6_address
        else:
            print(f"[ERROR] 直接IPv6连接失败: {ipv6_address}:{port} (错误码: {result})")
            return None
    except Exception as e:
        print(f"[ERROR] 直接IPv6连接异常: {e}")
        return None

def test_modified_connection(ip_address):
    """使用IP地址而不是主机名连接"""
    if not ip_address:
        print("[ERROR] 无法获取IP地址")
        return
    
    print(f"\n=== 使用IP地址连接测试 ===")
    
    # 构建新的连接字符串
    original_url = "postgresql://postgres:huangzhixin2025@db.wjuaayjnetykmnyqejhi.supabase.co:5432/postgres"
    modified_url = original_url.replace("db.wjuaayjnetykmnyqejhi.supabase.co", ip_address)
    
    print(f"原始URL: {original_url.replace('huangzhixin2025', '***')}")
    print(f"修改后URL: {modified_url.replace('huangzhixin2025', '***')}")
    
    try:
        # 尝试连接
        conn = psycopg2.connect(modified_url)
        print("[OK] 数据库连接成功！")
        
        # 测试查询
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"[OK] PostgreSQL版本: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"[ERROR] 数据库连接失败: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] 其他错误: {e}")
        return False

def main():
    """主函数"""
    print("开始强制IPv4连接测试...")
    print("=" * 50)
    
    # 测试直接IPv6连接
    ip_address = test_ipv4_connection()
    
    if ip_address:
        # 尝试使用IP地址连接数据库
        success = test_modified_connection(ip_address)
        if success:
            print("\n[SUCCESS] 数据库连接成功！可以上线了！")
        else:
            print("\n[ERROR] 数据库连接仍然失败")
    else:
        print("\n[ERROR] 无法建立网络连接")
    
    print("\n" + "=" * 50)
    print("测试完成")

if __name__ == "__main__":
    main()
