from django.urls import path
from . import views

app_name = 'Pythonfun'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.index_view, name='index'),
    path('category/<str:slug>/', views.category_view, name='category'),
    path('manage/category-management/', views.category_management_view, name='category_management'),
    path('manage/article-edit/', views.article_edit_view, name='article_edit'),
    path('manage/course-management/', views.course_management_view, name='course_management'),
    
    # 前台页面路由
    path('tutorial/<int:pk>/', views.tutorial_detail_view, name='tutorial_detail'),
    
    # API 路由 - 分类管理
    path('api/main-categories/', views.main_category_api, name='main_category_api'),
    path('api/main-categories/<int:pk>/', views.main_category_detail_api, name='main_category_detail_api'),
    path('api/sub-categories/', views.sub_category_api, name='sub_category_api'),
    path('api/sub-categories/<int:pk>/', views.sub_category_detail_api, name='sub_category_detail_api'),
    
    # API 路由 - 文章管理
    path('api/articles/', views.article_api, name='article_api'),
    path('api/articles/<int:pk>/', views.article_detail_api, name='article_detail_api'),
    
    # API 路由 - 教程管理
    path('api/courses/', views.course_api, name='course_api'),
    path('api/courses/<int:pk>/', views.course_detail_api, name='course_detail_api'),
    path('api/courses/<int:pk>/publish/', views.course_publish_api, name='course_publish_api'),
    
    # 导航栏页面路由
    path('function-library/', views.function_library_view, name='function_library'),
    path('function-query/', views.function_query_view, name='function_query'),
    path('data-structure/', views.data_structure_view, name='data_structure'),
    path('statement/', views.statement_view, name='statement'),
    path('project/', views.project_view, name='project'),
]