
import matplotlib
matplotlib.use('Agg')  # 设置无头后端
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.utils import timezone  # 导入用于获取当前时间的模块
def login(request):
    if request.method == 'GET':
        # 清空 session
        request.session.flush()
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        # 检查用户名是否存在
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse('no exist')

        # 验证密码是否正确
        if check_password(password, user.password):
            # 更新最近登录时间
            user.last_login = timezone.now()
            user.save()
            request.session['user_id'] = user.id  # 记录用户登录状态
            return redirect('/myapp/index')  # 登录成功后跳转到首页
        else:
            return HttpResponse('wrong PWD')

# 新用户注册
def regist(request):
    if request.method == 'GET':
        return render(request, 'regist.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        password_question = request.POST['password_question']
        password_answer = request.POST['password_answer']
        bio = request.POST.get('bio', 'bro is sleepy')  # 个人介绍是可选字段

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return HttpResponse('already exist')

        # 创建新用户并保存
        User.objects.create(
            username=username,
            password=make_password(password),  # 密码加密
            email=email,
            password_question=password_question,
            password_answer=password_answer,
            bio=bio
        )

        # 注册成功后重定向到登录页面
        return redirect('/myapp/login')

# 新用户找回密码
# 密码重置 两部分实现
def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # 第一阶段：用户提交邮箱，查询密码问题
        if 'password_question' not in request.POST:
            try:
                user = User.objects.get(email=email)
                # 渲染页面时显示密码问题
                return render(request, 'password_reset.html', {
                    'email': email,
                    'password_question': user.password_question
                })
            except User.DoesNotExist:
                return HttpResponse('no email')

        # 第二阶段：用户回答密码问题并输入新密码
        else:
            password_answer = request.POST.get('password_answer')
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')

            # 再次获取用户
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return HttpResponse('no email')

            # 检查密码问题答案是否正确
            if user.password_answer != password_answer:
                return HttpResponse('wrong answer')

            # 检查新密码和确认密码是否匹配
            if new_password != confirm_new_password:
                return HttpResponse('PWD not match')

            # 设置新密码并保存
            user.password = make_password(new_password)
            user.save()

            return HttpResponse('Password reset successful! Please return to the login page.')

    # 如果是 GET 请求，渲染初始的密码重置页面
    return render(request, 'password_reset.html')
from django.http import JsonResponse

from django.contrib.auth.hashers import make_password
# 用户提交密保问题和邮箱成功后，将会跳转到输入新密码的界面
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password_answer = request.POST.get('password_answer')
        new_password = request.POST.get('new_password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'success': False})

        # 验证密码问题答案是否正确
        if user.password_answer == password_answer:
            user.password = make_password(new_password)  # 设置新密码
            user.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

# 超级管理员登录
def admin_login(request):
    if request.method == 'GET':
        # 清空 session
        request.session.flush()
        return render(request, 'admin_login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        # 检查用户名是否存在
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse('not exist')

        # 验证密码是否正确
        if check_password(password, user.password):
            # 检查是否为超级管理员
            if user.is_super_admin:
                # 这里的seseion中保存的id和普通用户存在差别
                # 普通用户如下
                # request.session['user_id'] = user.id  # 记录用户登录状态
                request.session['admin_user_id'] = user.id
                return redirect('/myapp/admin_dashboard')  # 重定向到管理员后台
            else:
                return HttpResponse('no right to access')
        else:
            return HttpResponse('密码错误')

def admin_dashboard(request):
    # 检查用户是否已登录并且是超级管理员
    if 'admin_user_id' not in request.session:
        return HttpResponse('no right to access')  # 普通用户或未登录的用户无法访问

    return render(request, 'admin_dashboard.html')

# 普通用户的功能
# 首页视图
def index(request):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    # 获取当前登录的用户
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    return render(request, 'index.html', {'user': user})

# 查看个人信息
def guest_profile_display(request):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    return render(request, 'guest_profile_display.html', {'user': user})

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import User

# 查看个人信息
def guest_profile_display(request):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    return render(request, 'guest_profile_display.html', {'user': user})

# 修改个人信息表单展示
def guest_profile_edit(request):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    return render(request, 'guest_profile_edit.html', {'user': user})

# 处理提交修改的个人信息
def guest_profile_edit_upload(request):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    if request.method == 'POST':
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)

        # 更新用户信息
        user.email = request.POST['email']
        user.bio = request.POST['bio']
        user.avatar = request.POST['avatar']
        user.password_question = request.POST['password_question']
        user.password_answer = request.POST['password_answer']

        # 如果用户输入了新密码，进行密码更新
        new_password = request.POST.get('password')
        if new_password:
            user.password = make_password(new_password)

        user.save()

        return redirect('/myapp/guest_profile_display')

    return HttpResponse("非法请求")

from django.shortcuts import render, redirect
from .models import Post,Loop
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
# 创建 Backer Log
# views.py
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Post, Loop
from django.db.models import Q

def create_backer_log(request):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    # 获取用户加入的所有圈子
    user_loops = Loop.objects.filter(
        Q(members__user=user) | Q(owner=user)
    ).distinct()

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        location = request.POST.get('location', '')
        price_range = request.POST.get('price_range', '')
        cuisine = request.POST.get('cuisine', '')
        rating = request.POST.get('rating', 0)  # 获取评分
        selected_loops = request.POST.getlist('loops')

        # 处理图片上传
        if 'image' in request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage()
            image_path = fs.save(image.name, image)
        else:
            image_path = None

        # 创建帖子
        post = Post.objects.create(
            title=title,
            content=content,
            location=location,
            price_range=price_range,
            cuisine=cuisine,
            image=image_path,
            author=user,
            rating=rating  # 设置评分
        )

        # 关联圈子
        if selected_loops:
            for loop_id in selected_loops:
                try:
                    loop = Loop.objects.get(id=loop_id)
                    post.loop = loop
                    post.save()
                except Loop.DoesNotExist:
                    continue

        messages.success(request, 'Backer Log created successfully!')

        return redirect('/myapp/feed')

    return render(request, 'create_backer_log.html', {'user_loops': user_loops})


def location_suggestions(request):
    query = request.GET.get('query', '')
    if query:
        # 从数据库中获取所有唯一的 Location
        suggestions = Post.objects.filter(location__icontains=query).values_list('location', flat=True).distinct()[:10]
    else:
        suggestions = []

    return JsonResponse(list(suggestions), safe=False)

# 创建圈子 (Loop)
def create_loop(request):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')
        is_public = request.POST.get('is_public') == 'on'
        is_paid = request.POST.get('is_paid') == 'on'
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)

        # 创建新的 Loop
        Loop.objects.create(
            name=name,
            description=description,
            owner=user,
            is_public=is_public,
            is_paid=is_paid
        )

        messages.success(request, 'Loop created successfully!')

        return redirect(f'/myapp/manage_loops')

    return render(request, 'create_loop.html')
from myapp.models import Loop, LoopMember, Post, PostInteraction, Comment, AdminActionLog
# 删除除了User表之外的所有信息
def delete_all_except_user(request):
    """
    删除所有表中的数据，除了 User 表
    """
    User.objects.all().delete()
    # 删除所有 Loop 相关数据
    LoopMember.objects.all().delete()
    Loop.objects.all().delete()

    # 删除所有 Post 相关数据
    PostInteraction.objects.all().delete()
    Comment.objects.all().delete()
    Post.objects.all().delete()

    # 删除 AdminActionLog 数据
    AdminActionLog.objects.all().delete()

    print("已删除所有表的数据，除了 User 表中的数据")
    return HttpResponse('success')

from django.shortcuts import render
from .models import Post, Loop

# Feed 页面视图 查看所有的帖子
# 在 views.py 中添加以下代码

from django.db.models import Count
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict
# views.py 中的代码修改
def get_recommended_posts(user_id):
    """
    基于协同过滤的推荐算法实现，带有降级策略
    """
    # 获取所有用户的交互数据
    interactions = PostInteraction.objects.all().values('user_id', 'post_id', 'is_liked', 'is_favorited')

    # 创建用户-物品交互矩阵
    user_item_matrix = defaultdict(lambda: defaultdict(float))

    # 填充交互矩阵
    for interaction in interactions:
        score = 0
        if interaction['is_liked']:
            score += 1
        if interaction['is_favorited']:
            score += 0.5
        user_item_matrix[interaction['user_id']][interaction['post_id']] = score

    # 如果用户没有任何交互，返回热门帖子
    if user_id not in user_item_matrix:
        return get_popular_posts()

    # 转换为numpy数组
    users = list(user_item_matrix.keys())
    items = list(set([item for user_items in user_item_matrix.values() for item in user_items]))

    matrix = np.zeros((len(users), len(items)))
    for i, user in enumerate(users):
        for j, item in enumerate(items):
            matrix[i][j] = user_item_matrix[user][item]

    # 计算用户相似度
    user_similarity = cosine_similarity(matrix)

    # 获取目标用户的索引
    try:
        user_idx = users.index(user_id)
    except ValueError:
        return get_popular_posts()

    # 获取相似用户
    similar_users = [(users[i], user_similarity[user_idx][i])
                     for i in range(len(users)) if i != user_idx]
    similar_users.sort(key=lambda x: x[1], reverse=True)
    similar_users = similar_users[:5]  # 取top 5相似用户

    # 获取推荐帖子
    recommended_posts = defaultdict(float)
    for similar_user_id, similarity in similar_users:
        user_interactions = PostInteraction.objects.filter(
            user_id=similar_user_id,
            is_liked=True
        ).select_related('post')

        for interaction in user_interactions:
            if not PostInteraction.objects.filter(
                    user_id=user_id,
                    post_id=interaction.post.id
            ).exists():
                recommended_posts[interaction.post.id] += similarity

    # 如果协同过滤没有产生足够的推荐结果，补充热门帖子
    recommended_post_ids = sorted(
        recommended_posts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    result_ids = [post_id for post_id, score in recommended_post_ids[:10]]

    if len(result_ids) < 5:  # 如果推荐结果太少，补充热门帖子
        popular_posts = get_popular_posts()
        result_ids.extend([post_id for post_id in popular_posts if post_id not in result_ids])
        result_ids = result_ids[:10]  # 确保最多返回10个结果

    return result_ids


def get_popular_posts():
    """
    获取热门帖子的函数
    基于点赞数、收藏数和评论数的综合排名
    """
    posts = Post.objects.annotate(
        like_count=Count('interactions', filter=Q(interactions__is_liked=True)),
        favorite_count=Count('interactions', filter=Q(interactions__is_favorited=True)),
        comment_count=Count('comments')
    ).order_by('-like_count', '-favorite_count', '-comment_count', '-created_at')[:10]

    return [post.id for post in posts]


# views.py
import re
from django.core.exceptions import ValidationError

# views.py
import re
from django.core.exceptions import ValidationError
from django.db.models import Q


def validate_price_range(price_range):
    """
    验证价格范围的函数
    支持的格式:
    1. 单个数字: "100"
    2. 范围格式: "100~300"
    返回 (price_type, start_price, end_price)
    """
    if not price_range:
        return None, None, None

    # 移除所有空格
    price_range = price_range.strip()

    # 验证单个数字
    if price_range.isdigit():
        price = int(price_range)
        if price <= 0:
            raise ValidationError("Price must be positive")
        return 'single', price, price

    # 验证范围格式 (例如 "100~300")
    range_pattern = r'^(\d+)~(\d+)$'
    match = re.match(range_pattern, price_range)
    if match:
        start = int(match.group(1))
        end = int(match.group(2))
        if start <= 0 or end <= 0:
            raise ValidationError("Prices must be positive")
        if start >= end:
            raise ValidationError("Starting price must be less than ending price")
        return 'range', start, end

    raise ValidationError("Invalid price format. Use either a single number or range format (e.g., '100' or '100~300')")


def feed(request):
    # 获取过滤器条件
    location = request.GET.get('location', '')
    cuisine = request.GET.get('cuisine', '')
    price_range = request.GET.get('price_range', '')
    show_recommendations = request.GET.get('recommend', '')

    # 基础查询集
    base_queryset = Post.objects.all()

    # 应用过滤条件
    if location:
        base_queryset = base_queryset.filter(location__icontains=location)
    if cuisine:
        base_queryset = base_queryset.filter(cuisine__icontains=cuisine)

    # 价格过滤逻辑
    if price_range:
        try:
            price_type, start_price, end_price = validate_price_range(price_range)

            filtered_posts = []
            for post in base_queryset:
                post_price_str = post.price_range
                if not post_price_str:
                    continue

                # 解析帖子的价格
                try:
                    if '~' in post_price_str:
                        post_start, post_end = map(int, post_price_str.split('~'))
                    else:
                        post_start = post_end = int(post_price_str)

                    # 检查价格是否匹配
                    if price_type == 'single':
                        # 单个价格需要落在帖子的价格范围内
                        if post_start <= start_price <= post_end:
                            filtered_posts.append(post.id)
                    else:
                        # 价格范围需要与帖子的价格范围有交集
                        if not (post_end < start_price or post_start > end_price):
                            filtered_posts.append(post.id)

                except ValueError:
                    continue  # 跳过无效的价格格式

            base_queryset = base_queryset.filter(id__in=filtered_posts)

        except ValidationError as e:
            messages.error(request, str(e))
            base_queryset = Post.objects.none()  # 返回空查询集

    if show_recommendations and 'user_id' in request.session:
        # 获取推荐的帖子
        recommended_post_ids = get_recommended_posts(request.session['user_id'])
        posts = base_queryset.filter(id__in=recommended_post_ids)
        # 保持推荐顺序
        posts = sorted(posts, key=lambda x: recommended_post_ids.index(x.id))
    else:
        # 按时间顺序显示所有帖子
        posts = base_queryset.order_by('-created_at')

    # 为每个帖子添加用户交互信息
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        for post in posts:
            interaction = PostInteraction.objects.filter(
                post=post,
                user_id=user_id
            ).first()
            post.user_interaction = interaction

    return render(request, 'feed.html', {
        'posts': posts,
        'show_recommendations': bool(show_recommendations),
        'has_interactions': PostInteraction.objects.filter(
            user_id=request.session.get('user_id', None)).exists() if 'user_id' in request.session else False
    })
# 圈子展示页面视图
from django.shortcuts import render, redirect
from .models import User, Loop
from django.contrib import messages

from django.shortcuts import render, redirect
from .models import Loop, LoopMember

from django.db.models import Count, Q
from django.shortcuts import render, redirect
from .models import Loop, LoopMember, Post, PostInteraction, Comment


def get_member_stats(member):
    """获取成员的统计信息"""
    user = member.user
    loop = member.loop

    # 在该圈子中的帖子数
    posts_count = Post.objects.filter(author=user, loop=loop).count()

    # 在该圈子中收到的赞、评论和收藏数
    post_ids = Post.objects.filter(author=user, loop=loop).values_list('id', flat=True)
    likes_count = PostInteraction.objects.filter(post_id__in=post_ids, is_liked=True).count()
    comments_count = Comment.objects.filter(post_id__in=post_ids).count()
    favorites_count = PostInteraction.objects.filter(post_id__in=post_ids, is_favorited=True).count()

    # 用户加入的总圈子数
    total_loops_joined = LoopMember.objects.filter(user=user).count()

    return {
        'username': user.username,
        'posts_count': posts_count,
        'likes_count': likes_count,
        'comments_count': comments_count,
        'favorites_count': favorites_count,
        'total_loops_joined': total_loops_joined
    }


def loop_list(request):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    user_id = request.session.get('user_id')
    search_query = request.GET.get('search', '')

    # 根据搜索查询获取圈子
    if search_query:
        loops = Loop.objects.filter(name__icontains=search_query)
    else:
        loops = Loop.objects.all()

    # 为每个圈子标记用户是否可以加入并获取成员统计信息
    for loop in loops:
        loop.is_owner = (loop.owner.id == user_id)
        loop.is_member = LoopMember.objects.filter(loop=loop, user_id=user_id).exists()
        loop.is_full = loop.members.count() >= loop.max_members

        # 获取该圈子所有成员的统计信息
        loop.member_stats = []
        for member in LoopMember.objects.filter(loop=loop):
            stats = get_member_stats(member)
            loop.member_stats.append(stats)

    return render(request, 'loop_list.html', {
        'loops': loops,
        'user_id': user_id
    })
# 普通用户管理自己创建的圈子和帖子
from django.shortcuts import render, get_object_or_404, redirect
from .models import Loop, Post, LoopMember, User

# 获取当前用户管理的圈子
from django.shortcuts import render, redirect
from .models import User, Loop

def manage_loops(request):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    # 获取当前用户管理的所有圈子
    user_loops = Loop.objects.filter(owner=user)

    # 传递圈子列表到模板
    return render(request, 'manage_loops.html', {'user_loops': user_loops})


# 管理指定圈子的帖子和成员
def manage_loop_details(request, loop_id):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    # 获取用户管理的指定圈子
    loop = get_object_or_404(Loop, id=loop_id, owner=user)

    # 获取该圈子的所有帖子和成员
    posts = loop.posts.all()
    members = loop.members.all()

    return render(request, 'manage_loop_details.html', {
        'loop': loop,
        'posts': posts,
        'members': members
    })


# 删除帖子
# def delete_post(request, post_id):
#     if 'user_id' not in request.session:
#         return redirect('/myapp/login')
#
#     post = get_object_or_404(Post, id=post_id)
#     loop_id = post.loop.id
#     post.delete()
#     return redirect('/myapp/manage_loop_details', loop_id=loop_id)


# 移除成员
def remove_member(request, loop_id, member_id):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    loop = get_object_or_404(Loop, id=loop_id, owner=user)
    member = get_object_or_404(LoopMember, id=member_id, loop=loop)
    member.delete()
    return redirect('/myapp/manage_loops')

from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Loop, LoopMember
from django.contrib import messages
# 加入圈子
def join_loop(request, loop_id):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    loop = get_object_or_404(Loop, id=loop_id)

    # 检查圈子成员数量是否已满
    if loop.members.count() >= loop.max_members:
        messages.error(request, '该圈子人数已满，无法加入。')
        return redirect('/myapp/loop_list')

    # 检查用户是否已经是该圈子的成员
    if not LoopMember.objects.filter(loop=loop, user=user).exists():
        LoopMember.objects.create(loop=loop, user=user)
        messages.success(request, 'Successfully joined the loop!')

    else:
        messages.info(request, 'You are already a member of this loop.')

    return redirect('/myapp/loop_list')

# 在帖子大厅实现评论
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post, Comment

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            user_id = request.session.get('user_id')
            if user_id:
                author = User.objects.get(id=user_id)
                Comment.objects.create(post=post, author=author, content=content)
                messages.success(request, 'Comment posted successfully!')
            else:
                messages.error(request, 'You must be logged in to post a comment!')
        else:
            messages.error(request, 'Comment content cannot be empty!')

    comments = post.comments.all()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

# 点赞点踩收藏的功能
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Post, PostInteraction, User


def post_like(request, post_id):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    post = get_object_or_404(Post, id=post_id)
    user_id = request.session['user_id']
    interaction, created = PostInteraction.objects.get_or_create(post=post, user_id=user_id)
    interaction.is_liked = not interaction.is_liked
    interaction.is_disliked = False if interaction.is_liked else interaction.is_disliked
    interaction.save()

    messages.success(request, f"You have {'liked' if interaction.is_liked else 'unliked'} this post.")

    return redirect('/myapp/feed')

def post_dislike(request, post_id):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    post = get_object_or_404(Post, id=post_id)
    user_id = request.session['user_id']
    interaction, created = PostInteraction.objects.get_or_create(post=post, user_id=user_id)
    interaction.is_disliked = not interaction.is_disliked
    interaction.is_liked = False if interaction.is_disliked else interaction.is_liked
    interaction.save()

    messages.success(request,
                     f"You have {'disliked' if interaction.is_disliked else 'removed your dislike from'} this post.")

    return redirect('/myapp/feed')

def post_favorite(request, post_id):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    post = get_object_or_404(Post, id=post_id)
    user_id = request.session['user_id']
    interaction, created = PostInteraction.objects.get_or_create(post=post, user_id=user_id)
    interaction.is_favorited = not interaction.is_favorited
    interaction.save()

    messages.success(request, f"You have {'favorited' if interaction.is_favorited else 'unfavorited'} this post.")

    return redirect('/myapp/feed')

# 用户的消息列表
from django.shortcuts import render
from .models import PostInteraction

from django.shortcuts import render
from .models import PostInteraction, Comment
from django.utils import timezone

def post_action_logs(request):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    user_id = request.session.get('user_id')

    # 获取针对当前用户帖子上的所有交互
    interactions = PostInteraction.objects.filter(post__author_id=user_id).select_related('user', 'post')
    comments = Comment.objects.filter(post__author_id=user_id).select_related('author', 'post')

    # 将点赞、点踩、收藏、评论都整合成一个动作日志列表
    action_logs = []

    for interaction in interactions:
        if interaction.is_liked:
            action_logs.append({
                'user': interaction.user,
                'post': interaction.post,
                'action_type': 'likes',
                'timestamp': interaction.post.created_at,
            })
        if interaction.is_disliked:
            action_logs.append({
                'user': interaction.user,
                'post': interaction.post,
                'action_type': 'dislikes',
                'timestamp': interaction.post.created_at,
            })
        if interaction.is_favorited:
            action_logs.append({
                'user': interaction.user,
                'post': interaction.post,
                'action_type': 'collected',
                'timestamp': interaction.post.created_at,
            })

    for comment in comments:
        action_logs.append({
            'user': comment.author,
            'post': comment.post,
            'action_type': 'commented',
            'timestamp': comment.created_at,
        })

    # 按时间倒序排序动作日志
    action_logs = sorted(action_logs, key=lambda x: x['timestamp'], reverse=True)

    return render(request, 'post_action_logs.html', {'action_logs': action_logs})

# 管理员对用户的信息做删除和查看
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('/myapp/user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})

# 在我加入的圈子中发布帖子
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Loop, Post, Comment, LoopMember

def my_loops(request):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    # 获取用户加入的圈子
    loops = Loop.objects.filter(members__user_id=user_id)

    # 获取用户管理的圈子，通过 Loop 表的 owner 字段
    managed_loops = Loop.objects.filter(owner=user)

    # 合并加入的圈子和管理的圈子，并确保去重
    all_loops = (loops | managed_loops).distinct()

    return render(request, 'my_loops.html', {'loops': all_loops})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Loop, Post, User
from django.core.files.storage import FileSystemStorage
# 在圈子内做帖子上传
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Post, Loop, User

def create_post(request, loop_id):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        location = request.POST.get('location', '')
        price_range = request.POST.get('price_range', '')
        cuisine = request.POST.get('cuisine', '')
        rating = request.POST.get('rating', 0)  # 获取评分
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        loop = get_object_or_404(Loop, id=loop_id)

        # 处理图片上传
        if 'image' in request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage()
            image_path = fs.save(image.name, image)
        else:
            image_path = None

        # 创建新的 Post
        Post.objects.create(
            title=title,
            content=content,
            location=location,
            price_range=price_range,
            cuisine=cuisine,
            image=image_path,
            author=user,
            loop=loop,
            rating=rating  # 保存评分
        )

        messages.success(request, 'Post created successfully!')
        return redirect('/myapp/my_loops')

    return render(request, 'create_post.html', {'loop_id': loop_id})




def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author.id == request.session.get('user_id'):
        post.delete()
        messages.success(request, 'Post deleted successfully!')
    return redirect('/myapp/my_loops')


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author.id == request.session.get('user_id'):
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
    return redirect('/myapp/my_loops')


def like_post(request, post_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/myapp/login')

    post = get_object_or_404(Post, id=post_id)
    interaction, created = PostInteraction.objects.get_or_create(post=post, user_id=user_id)
    interaction.is_liked = True
    interaction.is_disliked = False
    interaction.save()

    messages.success(request, 'You liked the post!')
    return redirect('/myapp/my_loops')


def dislike_post(request, post_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/myapp/login')

    post = get_object_or_404(Post, id=post_id)
    interaction, created = PostInteraction.objects.get_or_create(post=post, user_id=user_id)
    interaction.is_disliked = True
    interaction.is_liked = False
    interaction.save()

    messages.success(request, 'You disliked the post!')
    return redirect('/myapp/my_loops')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Post, Comment, User
# 发表评论
def comment(request, post_id):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    if request.method == 'POST':
        content = request.POST['content']
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)
        post = get_object_or_404(Post, id=post_id)

        # 创建新的评论
        Comment.objects.create(
            post=post,
            author=user,
            content=content
        )

        messages.success(request, 'Comment added successfully!')
        return redirect('/myapp/my_loops')


from django.shortcuts import render
from django.db.models import Count, Q
from .models import Post, PostInteraction, Comment

from django.shortcuts import render
from django.db.models import Count, Q
from .models import Post


def explore_locations(request):
    # 获取所有有地点信息的帖子，并统计每个地点的帖子数量、总点赞数和评论数
    locations_queryset = (
        Post.objects
        .filter(location__isnull=False)
        .values('location')
        .annotate(
            post_count=Count('id'),
            total_likes=Count('interactions', filter=Q(interactions__is_liked=True)),
            total_comments=Count('comments')
        )
    )

    # 将 QuerySet 转换为列表，以便前端可以轻松使用
    locations = list(locations_queryset)

    return render(request, 'explore_locations.html', {'locations': locations})


from django.db.models import Avg
from django.shortcuts import render

def posts_at_location(request):
    location_name = request.GET.get('location')
    posts = Post.objects.filter(location=location_name)
    average_rating = posts.aggregate(Avg('rating'))['rating__avg']  # 计算平均评分
    return render(request, 'posts_at_location.html', {'posts': posts, 'location': location_name, 'average_rating': average_rating})

# AA功能
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import SplitBill, SplitBillParticipant, User

def create_split_bill(request):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        participants_ids = request.POST.getlist('participants')

        # 创建分账
        bill = SplitBill.objects.create(
            created_by=user,
            amount=amount,
            description=description
        )

        # 添加参与者
        for participant_id in participants_ids:
            participant = User.objects.get(id=participant_id)
            SplitBillParticipant.objects.create(bill=bill, user=participant)

        messages.success(request, 'Split bill created successfully!')

        return redirect('/myapp/view_split_bills')

    # 获取所有用户作为分账参与者选择
    users = User.objects.all()
    return render(request, 'create_split_bill.html', {'users': users})

def view_split_bills(request):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    # 获取用户相关的所有分账
    bills = SplitBillParticipant.objects.filter(user=user)

    return render(request, 'view_split_bills.html', {'bills': bills})

def pay_bill(request, bill_id):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    user_id = request.session['user_id']
    participant = get_object_or_404(SplitBillParticipant, bill_id=bill_id, user_id=user_id)

    if participant.has_paid:
        messages.info(request, 'You have already made the payment!')

    else:
        participant.has_paid = True
        participant.paid_at = timezone.now()
        participant.save()
        messages.success(request, 'Payment successful!')

    return redirect('/myapp/view_split_bills')

from django.shortcuts import render, redirect
from .models import SplitBill, SplitBillParticipant, User

def view_created_bills(request):
    if 'user_id' not in request.session:
        return redirect('/myapp/login')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    # 获取用户创建的所有分账
    created_bills = SplitBill.objects.filter(created_by=user)

    return render(request, 'view_created_bills.html', {'created_bills': created_bills})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Loop
from django.contrib import messages

# 查看所有帖子
def admin_view_posts(request):

    posts = Post.objects.all()
    return render(request, 'admin_view_posts.html', {'posts': posts})

# 删除帖子
def admin_delete_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('admin_view_posts')

# 查看所有评论
def admin_view_comments(request):

    comments = Comment.objects.all()
    return render(request, 'admin_view_comments.html', {'comments': comments})

# 删除评论
def admin_delete_comment(request, comment_id):

    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect('admin_view_comments')

# 查看所有圈子
def admin_view_loops(request):

    loops = Loop.objects.all()
    return render(request, 'admin_view_loops.html', {'loops': loops})

# 删除圈子
def admin_delete_loop(request, loop_id):

    loop = get_object_or_404(Loop, id=loop_id)
    loop.delete()
    messages.success(request, "Loop deleted successfully.")
    return redirect('admin_view_loops')
