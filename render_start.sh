#!/bin/bash
# Render启动脚本 - 简化版本
echo "开始启动Django应用..."

# 设置环境变量
export DJANGO_SETTINGS_MODULE=mysite.settings
export DEBUG=False

# 启动应用
echo "启动gunicorn..."
gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
