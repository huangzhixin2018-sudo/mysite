#!/usr/bin/env python3
"""
直接测试PostgreSQL数据库连接
"""
import os
import socket
import psycopg2
from urllib.parse import urlparse

def test_dns_resolution():
    """测试DNS解析"""
    print("=== DNS解析测试 ===")
    hostname = "db.wjuaayjnetykmnyqejhi.supabase.co"
    
    try:
        # 获取所有IP地址
        ipv4_addresses = socket.gethostbyname_ex(hostname)
        print(f"[OK] IPv4地址: {ipv4_addresses[2]}")
    except socket.gaierror as e:
        print(f"[ERROR] IPv4解析失败: {e}")
    
    try:
        # 获取IPv6地址
        ipv6_addresses = socket.getaddrinfo(hostname, None, socket.AF_INET6)
        ipv6_list = list(set(addr[4][0] for addr in ipv6_addresses))
        print(f"[OK] IPv6地址: {ipv6_list}")
    except socket.gaierror as e:
        print(f"[ERROR] IPv6解析失败: {e}")

def test_socket_connection():
    """测试Socket连接"""
    print("\n=== Socket连接测试 ===")
    hostname = "db.wjuaayjnetykmnyqejhi.supabase.co"
    port = 5432
    
    try:
        # 尝试IPv4连接
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((hostname, port))
        sock.close()
        
        if result == 0:
            print(f"[OK] IPv4连接成功: {hostname}:{port}")
        else:
            print(f"[ERROR] IPv4连接失败: {hostname}:{port} (错误码: {result})")
    except Exception as e:
        print(f"[ERROR] IPv4连接异常: {e}")
    
    try:
        # 尝试IPv6连接
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((hostname, port))
        sock.close()
        
        if result == 0:
            print(f"[OK] IPv6连接成功: {hostname}:{port}")
        else:
            print(f"[ERROR] IPv6连接失败: {hostname}:{port} (错误码: {result})")
    except Exception as e:
        print(f"[ERROR] IPv6连接异常: {e}")

def test_psycopg2_connection():
    """测试psycopg2连接"""
    print("\n=== psycopg2连接测试 ===")
    
    # 从环境变量获取数据库URL
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("[ERROR] DATABASE_URL 环境变量未设置")
        return
    
    # 解析数据库URL
    parsed = urlparse(database_url)
    print(f"主机: {parsed.hostname}")
    print(f"端口: {parsed.port}")
    print(f"数据库: {parsed.path[1:]}")
    print(f"用户: {parsed.username}")
    
    try:
        # 尝试连接
        conn = psycopg2.connect(database_url)
        print("[OK] 数据库连接成功！")
        
        # 测试查询
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"[OK] PostgreSQL版本: {version[0]}")
        
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"[ERROR] 数据库连接失败: {e}")
    except Exception as e:
        print(f"[ERROR] 其他错误: {e}")

def main():
    """主函数"""
    print("开始PostgreSQL连接测试...")
    print("=" * 50)
    
    test_dns_resolution()
    test_socket_connection()
    test_psycopg2_connection()
    
    print("\n" + "=" * 50)
    print("测试完成")

if __name__ == "__main__":
    main()
