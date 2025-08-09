#!/bin/bash
# Render构建脚本
pip install -r requirements.txt
python manage.py collectstatic --noinput
