#!/bin/bash
# Render构建脚本
echo "开始构建..."

# 安装依赖
echo "安装Python依赖..."
pip install -r requirements.txt

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

echo "构建完成！"
