import json
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import MainCategory, SubCategory, Article, Tag

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

# ========== 页面渲染视图 ==========

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Pythonfun:category_management') # 使用URL名称进行重定向
        else:
            messages.error(request, '用户名或密码无效')
            return render(request, 'admin/登录.html', status=401)
    return render(request, 'admin/登录.html')

def index_view(request):
    """首页视图 - 显示分类树和默认第一篇文章"""
    main_categories = MainCategory.objects.filter(is_enabled=True).order_by('order')
    category_tree = []
    for main_category in main_categories:
        sub_categories = SubCategory.objects.filter(
            parent=main_category,
            is_enabled=True
        ).order_by('id')
        sub_categories_with_count = []
        for sub in sub_categories:
            article_count = Article.objects.filter(
                category=sub,
                content_type=Article.ContentType.TUTORIAL,
                is_published=True
            ).count()
            sub.article_count = article_count
            sub_categories_with_count.append(sub)
        category_tree.append({
            'main_category': main_category,
            'sub_categories': sub_categories_with_count
        })
    current_article = Article.objects.filter(
        content_type=Article.ContentType.TUTORIAL,
        is_published=True
    ).order_by('created_at').first()
    context = {
        'category_tree': category_tree,
        'current_article': current_article,
    }
    return render(request, 'front/index.html', context)

def category_view(request, slug):
    """子分类文章显示视图"""
    main_categories = MainCategory.objects.filter(is_enabled=True).order_by('order')
    category_tree = []
    for main_category in main_categories:
        sub_categories = SubCategory.objects.filter(
            parent=main_category,
            is_enabled=True
        ).order_by('id')
        sub_categories_with_count = []
        for sub in sub_categories:
            article_count = Article.objects.filter(
                category=sub,
                content_type=Article.ContentType.TUTORIAL,
                is_published=True
            ).count()
            sub.article_count = article_count
            sub_categories_with_count.append(sub)
        category_tree.append({
            'main_category': main_category,
            'sub_categories': sub_categories_with_count
        })
    try:
        current_category = SubCategory.objects.get(slug=slug)
    except SubCategory.DoesNotExist:
        return render(request, 'front/404.html', status=404)
    current_article = Article.objects.filter(
        category=current_category,
        content_type=Article.ContentType.TUTORIAL,
        is_published=True
    ).order_by('created_at').first()
    context = {
        'category_tree': category_tree,
        'current_category': current_category,
        'current_article': current_article,
    }
    return render(request, 'front/index.html', context)

@login_required
def category_management_view(request):
    return render(request, 'admin/分类管理.html')

@login_required
def article_edit_view(request):
    article_id = request.GET.get('id')
    article = None
    if article_id:
        article = get_object_or_404(Article, id=article_id)
    return render(request, 'admin/文章编辑.html', {'article': article})

@login_required
def course_management_view(request):
    return render(request, 'admin/教程管理.html')

def tutorial_detail_view(request, pk):
    tutorial = get_object_or_404(Article, pk=pk)
    is_admin = request.user.is_authenticated and request.user.is_staff
    if not tutorial.is_published and not is_admin:
        return render(request, 'front/404.html', {'error_message': '教程不存在或未发布'})

    related_tutorials = Article.objects.filter(
        category=tutorial.category, content_type=Article.ContentType.TUTORIAL, is_published=True
    ).exclude(pk=pk)[:5]
    
    context = {
        'tutorial': tutorial,
        'related_tutorials': related_tutorials,
        'is_admin': is_admin
    }
    return render(request, 'front/tutorial_detail.html', context)

# ========== API 视图 ==========

@require_http_methods(["GET", "POST"])
def main_category_api(request):
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        page_size = 10
        
        categories = MainCategory.objects.all().order_by('order')
        
        # 添加分页
        paginator = Paginator(categories, page_size)
        try:
            categories_page = paginator.page(page)
        except EmptyPage:
            categories_page = paginator.page(paginator.num_pages)
        
        data = {
            'items': list(categories_page.object_list.values('id', 'name', 'slug', 'order', 'is_enabled')),
            'current_page': categories_page.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count
        }
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            main_category = MainCategory.objects.create(
                name=data['name'],
                slug=data['slug'],
                order=data.get('order', 0),
                is_enabled=data.get('is_enabled', True)
            )
            return JsonResponse({
                'status': 'success', 
                'message': 'Main category created successfully', 
                'id': main_category.id
            }, status=201)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def main_category_detail_api(request, pk):
    main_category = get_object_or_404(MainCategory, pk=pk)
    if request.method == 'GET':
        data = {
            'id': main_category.id,
            'name': main_category.name,
            'order': main_category.order,
            'is_enabled': main_category.is_enabled
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        main_category.name = data.get('name', main_category.name)
        main_category.slug = data.get('slug', main_category.slug)
        main_category.order = data.get('order', main_category.order)
        main_category.is_enabled = data.get('is_enabled', main_category.is_enabled)
        main_category.save()
        return JsonResponse({'status': 'success', 'message': 'Main category updated successfully'})
    elif request.method == 'DELETE':
        main_category.delete()
        return JsonResponse({'status': 'success', 'message': 'Main category deleted successfully'})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def sub_category_api(request):
    if request.method == 'GET':
        main_category_id = request.GET.get('main_category_id')
        page = request.GET.get('page', 1)
        page_size = 10 # Assuming a default page size

        categories = SubCategory.objects.all()
        if main_category_id:
            categories = categories.filter(parent_id=main_category_id)

        # Add pagination
        paginator = Paginator(categories, page_size)
        try:
            categories_page = paginator.page(page)
        except EmptyPage:
            categories_page = paginator.page(paginator.num_pages)

        data = {
            'items': [{
                'id': cat.id,
                'name': cat.name,
                'slug': cat.slug,
                'parent_id': cat.parent.id if cat.parent else None,
                'parent_name': cat.parent.name if cat.parent else None,
                'is_enabled': cat.is_enabled
            } for cat in categories_page.object_list],
            'current_page': categories_page.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count
        }
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        parent_id = data.get('parent_id')
        parent_category = get_object_or_404(MainCategory, pk=parent_id) if parent_id else None
        sub_category = SubCategory.objects.create(
            name=data['name'],
            slug=data['slug'],
            parent=parent_category,
            is_enabled=data.get('is_enabled', True)
        )
        return JsonResponse({'status': 'success', 'message': 'Sub category created successfully', 'id': sub_category.id}, status=201)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def sub_category_detail_api(request, pk):
    sub_category = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'GET':
        data = {
            'id': sub_category.id,
            'name': sub_category.name,
            'parent_id': sub_category.parent.id if sub_category.parent else None,
            'is_enabled': sub_category.is_enabled
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        sub_category.name = data.get('name', sub_category.name)
        if 'parent_id' in data:
            parent_id = data.get('parent_id')
            if parent_id:
                sub_category.parent = get_object_or_404(MainCategory, pk=parent_id)
            else:
                sub_category.parent = None
        sub_category.is_enabled = data.get('is_enabled', sub_category.is_enabled)
        sub_category.save()
        return JsonResponse({'status': 'success', 'message': 'Sub category updated successfully'})
    elif request.method == 'DELETE':
        sub_category.delete()
        return JsonResponse({'status': 'success', 'message': 'Sub category deleted successfully'})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def article_api(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        data = [{
            'id': article.id,
            'title': article.title,
            'subtitle': article.subtitle,
            'summary': article.summary,
            'read_time_minutes': article.read_time_minutes,
            'is_published': article.is_published,
            'created_at': article.created_at.isoformat(),
            'updated_at': article.updated_at.isoformat(),
            'category_name': article.category.name if article.category else None,
            'tags': [tag.name for tag in article.tags.all()]
        } for article in articles]
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        article = Article.objects.create(
            title=data['title'],
            subtitle=data.get('subtitle', ''),
            summary=data.get('summary', ''),
            content_html=data.get('content_html', ''),
            content_code=data.get('content_code', ''),
            code_language=data.get('code_language', ''),
            content_type=data.get('content_type', Article.ContentType.TUTORIAL),
            read_time_minutes=data.get('read_time_minutes', 5),
            is_published=data.get('is_published', False)
        )
        if data.get('category_id'):
            article.category = get_object_or_404(SubCategory, pk=data.get('category_id'))
        article.save()
        if data.get('tags'):
            article.tags.set(Tag.objects.filter(name__in=data.get('tags')))
        return JsonResponse({'status': 'success', 'message': 'Article created successfully', 'id': article.id}, status=201)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def article_detail_api(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        data = {
            'id': article.id,
            'title': article.title,
            'subtitle': article.subtitle,
            'summary': article.summary,
            'read_time_minutes': article.read_time_minutes,
            'content_html': article.content_html,
            'content_code': article.content_code,
            'code_language': article.code_language,
            'category_id': article.category.id if article.category else None,
            'tags': [tag.name for tag in article.tags.all()],
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        article.title = data.get('title', article.title)
        article.subtitle = data.get('subtitle', article.subtitle)
        article.summary = data.get('summary', article.summary)
        article.read_time_minutes = data.get('read_time_minutes', article.read_time_minutes)

        article.content_html = data.get('content_html', article.content_html)
        article.content_code = data.get('content_code', article.content_code)
        article.code_language = data.get('code_language', article.code_language)
        if data.get('category_id'):
            article.category = get_object_or_404(SubCategory, pk=data.get('category_id'))
        article.save()
        article.tags.set(Tag.objects.filter(name__in=data.get('tags', [])))
        return JsonResponse({'status': 'success', 'message': 'Article updated successfully'})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def course_api(request):
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        page_size = 10 # Assuming a default page size

        courses = Article.objects.filter(content_type=Article.ContentType.TUTORIAL)

        # Add pagination
        paginator = Paginator(courses, page_size)
        try:
            courses_page = paginator.page(page)
        except EmptyPage:
            courses_page = paginator.page(paginator.num_pages)

        data = {
            'items': [{
                'id': course.id,
                'title': course.title,
                'subtitle': course.subtitle,
                'summary': course.summary,
                'read_time_minutes': course.read_time_minutes,
                'is_published': course.is_published,
                'created_at': course.created_at.isoformat(),
                'updated_at': course.updated_at.isoformat(),
                'category_name': course.category.name if course.category else None,
                'tags': [tag.name for tag in course.tags.all()]
            } for course in courses_page.object_list],
            'current_page': courses_page.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count
        }
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        course = Article.objects.create(
            title=data['title'],
            subtitle=data.get('subtitle', ''),
            summary=data.get('summary', ''),
            read_time_minutes=data.get('read_time_minutes', 0),
            content_html=data.get('content_html', ''),
            content_code=data.get('content_code', ''),
            code_language=data.get('code_language', ''),
            content_type=Article.ContentType.TUTORIAL,
            is_published=data.get('is_published', False)
        )
        if data.get('category_id'):
            course.category = get_object_or_404(SubCategory, pk=data.get('category_id'))
        course.save()
        if data.get('tags'):
            course.tags.set(Tag.objects.filter(name__in=data.get('tags')))
        return JsonResponse({'status': 'success', 'message': 'Course created successfully', 'id': course.id}, status=201)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def course_detail_api(request, pk):
    course = get_object_or_404(Article, pk=pk, content_type=Article.ContentType.TUTORIAL)
    if request.method == 'GET':
        data = {
            'id': course.id,
            'title': course.title,
            'subtitle': course.subtitle,
            'summary': course.summary,
            'read_time_minutes': course.read_time_minutes,
            'content_html': course.content_html,
            'content_code': course.content_code,
            'code_language': course.code_language,
            'category_id': course.category.id if course.category else None,
            'category_name': course.category.name if course.category else None,
            'tags': [tag.name for tag in course.tags.all()],
            'is_published': course.is_published,
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        course.title = data.get('title', course.title)
        course.subtitle = data.get('subtitle', course.subtitle)
        course.summary = data.get('summary', course.summary)
        course.read_time_minutes = data.get('read_time_minutes', course.read_time_minutes)

        course.content_html = data.get('content_html', course.content_html)
        course.content_code = data.get('content_code', course.content_code)
        course.code_language = data.get('code_language', course.code_language)
        if data.get('category_id'):
            course.category = get_object_or_404(SubCategory, pk=data.get('category_id'))
        course.save()
        course.tags.set(Tag.objects.filter(name__in=data.get('tags', [])))
        return JsonResponse({'status': 'success', 'message': 'Course updated successfully'})
    elif request.method == 'DELETE':
        try:
            # 记录删除的教程信息用于日志
            course_title = course.title
            course_id = course.id
            
            # 删除教程
            course.delete()
            
            return JsonResponse({
                'status': 'success', 
                'message': f'教程 "{course_title}" 已成功删除',
                'deleted_id': course_id
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'删除教程失败: {str(e)}'
            }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def course_publish_api(request, pk):
    course = get_object_or_404(Article, pk=pk, content_type=Article.ContentType.TUTORIAL)
    data = json.loads(request.body)
    is_published = data.get('is_published')
    if is_published is not None:
        course.is_published = is_published
        course.save()
        return JsonResponse({'status': 'success', 'message': 'Course publish status updated successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# ========== 导航栏页面视图 ==========

def function_library_view(request):
    """函数库页面视图"""
    return render(request, 'front/函数库.html')

def function_query_view(request):
    """函数查询页面视图"""
    return render(request, 'front/函数查询.html')

def data_structure_view(request):
    """数据结构页面视图"""
    return render(request, 'front/数据结构.html')

def statement_view(request):
    """语句页面视图"""
    return render(request, 'front/语句.html')

def project_view(request):
    """项目页面视图"""
    return render(request, 'front/项目.html')