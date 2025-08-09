from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from . import minimal_test_views

urlpatterns = [
    # 测试路由 - 不依赖数据库（Dummy模式）
    path('', minimal_test_views.welcome_page, name='welcome_page'),
    path('test/health/', minimal_test_views.health_check, name='health_check'),
    path('test/system/', minimal_test_views.system_info, name='system_info'),
    path('test/api/', minimal_test_views.api_test, name='api_test'),
]
