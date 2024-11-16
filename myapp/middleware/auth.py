from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
import re
class AuthMiddleware(MiddlewareMixin):
    """
    中间件，用于控制用户和管理员的访问权限。
    如果 session 中存在 admin_user_id 或 user_id，则允许访问。
    如果没有，则根据路径跳转到相应的登录页面。
    """

    def __call__(self, request):
        # 获取当前访问的路径
        path = request.path_info

        # 允许不需要拦截的路径列表
        allowed_paths = [
            '/myapp/admin_login',
            '/myapp/login',
            '/myapp/regist',
            '/myapp/password_reset',
            '/myapp/reset_password'
        ]

        # 1. 检查是否为不需要拦截的路径，直接放行
        if path in allowed_paths:
            return self.get_response(request)

        # 2. 如果 session 中有 admin_user_id 或 user_id，则不拦截，允许访问
        if 'admin_user_id' in request.session or 'user_id' in request.session:
            return self.get_response(request)

        # 3. 如果 session 中没有 admin_user_id 并且访问的是管理员相关路径，重定向到管理员登录页面
        if path.startswith('/myapp/admin'):
            return redirect('/myapp/login')

        # 4. 如果 session 中没有 user_id 并且访问的是普通用户相关页面，重定向到普通用户登录页面
        return redirect('/myapp/login')