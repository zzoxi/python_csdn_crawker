from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Info
from .models import Category
from . import crawker
from django.utils import timezone
# Create your views here.


def index(request):
    return render(request, 'info_assistant/index.html')


def search(request):
    key_word = request.POST['keyword']
    results = crawker.get_results(key_word)
    infos = results.get('infos')
    data_analysis = results.get('data_analysis')
    d_time = timezone.now()
    category = Category.objects.create(title=key_word, create_time=d_time)
    for i in infos:
        Info.objects.create(
            title=i.get('title'),
            search_key=i.get('keyword'),
            url=i.get('url'),
            source=i.get('source'),
            category=category,
            create_time=d_time,
        )
    info_list = Info.objects.filter(category=category)
    return render(request, 'info_assistant/details.html', {'info_list': info_list, 'analysis_list': data_analysis})


# 删除收藏夹里面的信息
def delete_info(request, info_id):
    Info.objects.filter(pk=info_id).delete()
    return HttpResponseRedirect('/show')


# 移动该条信息到
def move_info_get(request, info_id):
    info = Info.objects.filter(nid=info_id).first()
    c_list = Category.objects.all()
    return render(request, 'info_assistant/move_info.html', {'info': info, 'category_list': c_list})


def move_info_post(request):
    nid = request.POST['info_id']
    new_id = request.POST['new_category_id']
    c = Category.objects.filter(pk=new_id).first()
    Info.objects.filter(pk=nid).update(category=c)
    return HttpResponseRedirect('/show')

# 按照创建时间倒序展示
def category_list(request):
    category_list = Category.objects.all().order_by('-create_time')
    return render(request, "info_assistant/myCollections.html", {'category_list': category_list})


# 展示全部的信息
def show_category(request, category_id):
    category = Category.objects.filter(pk=category_id).first()
    infos = Info.objects.filter(category=category)
    return render(request, 'info_assistant/details.html', {'info_list': infos})


# 创建一个收藏夹
def create_category(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        Category.objects.create(title=category_name, create_time=timezone.now())
        return HttpResponseRedirect('/show')
    else:
        return render(request, 'info_assistant/create_category.html')


# 编辑收藏夹标题
def edit_category_post(request):
    category_id = request.POST.get('category_id')
    new_title = request.POST.get("new_title")
    print(category_id)
    Category.objects.filter(nid=category_id).update(title=new_title)
    return HttpResponseRedirect('/show')


def edit_category_get(request, id):
    return render(request, 'info_assistant/edit_category.html', {'id': id})


# 删除整个收藏夹
def delete_category(request, delete_id):
    Category.objects.get(pk=delete_id).delete()
    return HttpResponseRedirect('/show')


def enter_admin(request):
    return redirect('/admin')
