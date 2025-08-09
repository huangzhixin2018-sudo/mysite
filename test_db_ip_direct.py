#!/usr/bin/env python3
"""
直接使用IP地址连接数据库测试
"""
import os
import psycopg2

def test_direct_ip_connection():
    """直接使用IP地址连接"""
    print("=== 直接IP地址连接测试 ===")
    
    # 直接使用IP地址的连接字符串
    ip_url = "postgresql://postgres:huangzhixin2025@[2406:da18:243:740a:b3a7:c514:1fb4:7520]:5432/postgres"
    
    print(f"连接URL: {ip_url.replace('huangzhixin2025', '***')}")
    
    try:
        # 尝试连接
        conn = psycopg2.connect(ip_url)
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

def test_alternative_connection():
    """尝试替代连接方法"""
    print("\n=== 替代连接方法测试 ===")
    
    # 尝试不同的连接参数
    connection_params = {
        'host': '2406:da18:243:740a:b3a7:c514:1fb4:7520',
        'port': 5432,
        'database': 'postgres',
        'user': 'postgres',
        'password': 'huangzhixin2025'
    }
    
    print(f"连接参数: {connection_params}")
    
    try:
        # 尝试连接
        conn = psycopg2.connect(**connection_params)
        print("[OK] 替代方法连接成功！")
        
        # 测试查询
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"[OK] PostgreSQL版本: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"[ERROR] 替代方法连接失败: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] 其他错误: {e}")
        return False

def main():
    """主函数"""
    print("开始直接IP地址连接测试...")
    print("=" * 50)
    
    # 测试直接IP连接
    success1 = test_direct_ip_connection()
    
    if not success1:
        # 尝试替代方法
        success2 = test_alternative_connection()
        
        if success2:
            print("\n[SUCCESS] 替代方法成功！可以上线了！")
        else:
            print("\n[ERROR] 所有连接方法都失败")
    else:
        print("\n[SUCCESS] 直接IP连接成功！可以上线了！")
    
    print("\n" + "=" * 50)
    print("测试完成")

if __name__ == "__main__":
    main()
