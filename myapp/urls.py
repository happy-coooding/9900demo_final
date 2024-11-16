from django.urls import path
from .import views
urlpatterns =[
    # 首页
    path('index', views.index),
    # 新登录
    path('login', views.login),
    # 新用户注册
    path('regist', views.regist),
    # 新用户密码找回
    path('password_reset', views.password_reset),
    path('reset_password', views.reset_password),
    # 超级管理员的登录入口
    path('admin_login', views.admin_login),
    path('admin_dashboard', views.admin_dashboard),
    # 普通用户实现对自己的信息的修改和展示
    path('guest_profile_display', views.guest_profile_display),
    path('guest_profile_edit', views.guest_profile_edit),
    path('guest_profile_edit_upload', views.guest_profile_edit_upload),
    # 创建帖子
    path('create_backer_log', views.create_backer_log),
    # 创建圈子
    path('create_loop', views.create_loop),
    # 删库
    path('delete_all_except_user', views.delete_all_except_user),
    # 所有的帖子展示
    path('feed', views.feed),
    # 所有的圈子展示
    path('loop_list', views.loop_list),
    # 用户管理自己的圈子
    path('manage_loops', views.manage_loops),
    path('manage_loop_details/<int:loop_id>', views.manage_loop_details),
    path('delete_post/<int:post_id>', views.delete_post),
    path('remove_member/<int:loop_id>/<int:member_id>', views.remove_member),
    # 加入圈子
    path('join_loop/<int:loop_id>', views.join_loop),
    # 添加评论
    path('post_detail/<int:post_id>', views.post_detail),
    path('post_detail/<int:post_id>/like/', views.post_like),
    path('post_detail/<int:post_id>/dislike/', views.post_dislike),
    path('post_detail/<int:post_id>/favorite/', views.post_favorite),
    path('post_action_logs', views.post_action_logs),
    # 管理员功能
    path('user_list', views.user_list),
    path('user_detail/<int:pk>', views.user_detail),
    path('user_delete/<int:pk>', views.user_delete),
    path('location_suggestions/', views.location_suggestions),
    # 在我参加的圈子中做喜欢 不喜欢 评论 查看
    path('my_loops/', views.my_loops, name='my_loops'),
    path('create_post/<int:loop_id>/', views.create_post, name='create_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike_post/<int:post_id>/', views.dislike_post, name='dislike_post'),
    # 在当前页面实现评论值传递
    path('comment/<int:post_id>/', views.comment, name='comment'),
    path('explore_locations/', views.explore_locations, name='explore_locations'),
    path('posts_at_location/', views.posts_at_location, name='posts_at_location'),
    # AA分账
    path('create_split_bill', views.create_split_bill, name='create_split_bill'),
    path('view_split_bills', views.view_split_bills, name='view_split_bills'),
    path('pay_bill/<int:bill_id>', views.pay_bill, name='pay_bill'),
    path('view_created_bills', views.view_created_bills, name='view_created_bills'),
    # 管理员管理所有的圈子和帖子
    path('admin/posts', views.admin_view_posts, name='admin_view_posts'),
    path('admin_delete_post/<int:post_id>/', views.admin_delete_post, name='admin_delete_post'),
    path('admin/comments', views.admin_view_comments, name='admin_view_comments'),
    path('admin_delete_comment/<int:comment_id>/', views.admin_delete_comment, name='admin_delete_comment'),
    path('admin/loops', views.admin_view_loops, name='admin_view_loops'),
    path('admin_delete_loop/<int:loop_id>/', views.admin_delete_loop, name='admin_delete_loop'),
]
