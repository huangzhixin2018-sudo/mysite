#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建测试教程数据的脚本
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from Pythonfun.models import MainCategory, SubCategory, Article, Tag
from django.contrib.auth.models import User

def create_test_data():
    """创建测试数据"""
    
    print("=== 创建测试数据 ===")
    
    # 1. 检查是否有主分类
    main_cat, created = MainCategory.objects.get_or_create(
        name='Python教程',
        defaults={
            'slug': 'python-tutorials',
            'description': 'Python编程相关教程',
            'order': 1,
            'is_enabled': True
        }
    )
    if created:
        print(f"✓ 创建主分类: {main_cat.name}")
    else:
        print(f"✓ 主分类已存在: {main_cat.name}")
    
    # 2. 检查是否有子分类
    sub_cat, created = SubCategory.objects.get_or_create(
        name='Python基础',
        defaults={
            'slug': 'python-basics',
            'description': 'Python基础知识教程',
            'parent': main_cat,
            'order': 1,
            'is_enabled': True
        }
    )
    if created:
        print(f"✓ 创建子分类: {sub_cat.name}")
    else:
        print(f"✓ 子分类已存在: {sub_cat.name}")
    
    # 3. 检查是否有教程
    tutorial, created = Article.objects.get_or_create(
        title='Python入门教程',
        defaults={
            'subtitle': '从零开始学习Python',
            'summary': '这是一个Python入门教程，适合初学者学习',
            'content_html': '<h1>Python入门教程</h1><p>欢迎学习Python编程！</p>',
            'content_code': 'print("Hello, Python!")',
            'code_language': 'python',
            'content_type': Article.ContentType.TUTORIAL,
            'category': sub_cat,
            'is_published': False
        }
    )
    if created:
        print(f"✓ 创建教程: {tutorial.title}")
    else:
        print(f"✓ 教程已存在: {tutorial.title}")
    
    # 4. 检查数据总数
    print(f"\n=== 数据统计 ===")
    print(f"主分类数量: {MainCategory.objects.count()}")
    print(f"子分类数量: {SubCategory.objects.count()}")
    print(f"教程数量: {Article.objects.filter(content_type=Article.ContentType.TUTORIAL).count()}")
    print(f"标签数量: {Tag.objects.count()}")
    
    # 5. 列出所有教程
    print(f"\n=== 教程列表 ===")
    tutorials = Article.objects.filter(content_type=Article.ContentType.TUTORIAL)
    for i, tut in enumerate(tutorials, 1):
        print(f"{i}. ID: {tut.id}, 标题: {tut.title}, 状态: {'已发布' if tut.is_published else '草稿'}")
    
    print("\n=== 测试数据创建完成 ===")
    print("现在可以测试删除功能了")

if __name__ == "__main__":
    create_test_data()
