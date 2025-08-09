#!/bin/bash

echo "🚀 开始部署到Vercel..."

# 检查是否安装了Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI未安装，正在安装..."
    npm install -g vercel
fi

# 检查是否已登录Vercel
if ! vercel whoami &> /dev/null; then
    echo "🔐 请先登录Vercel账户..."
    vercel login
fi

# 检查Python环境
echo "🐍 检查Python环境..."
python --version

# 检查Django项目
echo "🔍 检查Django项目..."
python manage.py check

# 收集静态文件
echo "📁 收集静态文件..."
python manage.py collectstatic --noinput

# 部署项目
echo "📦 正在部署项目..."
vercel --prod

echo "✅ 部署完成！"
echo "🌐 您的应用已部署到Vercel"
echo "📝 如果遇到问题，请检查Vercel Dashboard的部署日志"
