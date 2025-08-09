#!/bin/bash
# Render启动脚本
python manage.py collectstatic --noinput
gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
