from django.urls import path

from . import views

# 命名空间
app_name = 'info_assistant'
urlpatterns = [

    # 搜索页面主页
    path('', views.index, name='index'),
    # 展示所有搜索结果
    path('search/', views.search, name="search"),
    # 从收藏夹里删除信息
    path('delete/<int:info_id>', views.delete_info, name="delete_info"),
    # 移动到其它收藏夹
    path('move/<int:info_id>', views.move_info_get, name="move_info"),
    # 表单
    path('move_post', views.move_info_post, name='move_info_post'),
    # 展示全部收藏夹
    path('show/', views.category_list, name='show'),
    # 展示收藏夹内容
    path('showall/<int:category_id>', views.show_category, name='showall'),
    # 创建收藏夹
    path('create/', views.create_category, name="create_category"),
    # 展示
    path('create_category/', views.create_category, name='create_category_get'),
    # 编辑收藏夹名称
    path('edit/', views.edit_category_post, name="edit_category"),
    # 展示编辑界面
    path('edit_interface/<int:id>', views.edit_category_get, name="edit_category_interface"),
    # 删除收藏夹
    path('delete_category/<int:delete_id>', views.delete_category, name="delete_category"),
    # 管理员界面
    path('enter_admin', views.enter_admin, name="enter_admin")
]