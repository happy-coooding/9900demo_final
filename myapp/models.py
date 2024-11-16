from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField("用户名", max_length=50, unique=True, null=False)
    password = models.CharField("密码", max_length=128, null=False)  # 建议使用加密方式存储
    email = models.EmailField("邮箱", max_length=100, unique=True, null=False)
    bio = models.CharField("个人介绍", max_length=500, null=True)
    avatar = models.CharField("头像url", max_length=200, null=True)
    date_joined = models.DateTimeField("注册时间", auto_now_add=True)
    last_login = models.DateTimeField("上次登录时间", auto_now=True)
    # 超级管理员标识
    is_super_admin = models.BooleanField("是否为超级管理员", default=False)
    # 用来找回密码
    password_question = models.CharField("密码问题", max_length=255, null=True, blank=True)
    password_answer = models.CharField("密码问题答案", max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username

class Loop(models.Model):
    name = models.CharField("圈子名", max_length=100, null=False)
    description = models.TextField("圈子描述", null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_loops")
    is_public = models.BooleanField("是否公开", default=True)
    is_paid = models.BooleanField("是否付费圈子", default=False)  # 新增字段，表明是否为付费圈子
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    max_members = models.IntegerField("成员最大数量", default=12)  # 新增字段，用于限制成员数量

    def __str__(self):
        return self.name


class LoopMember(models.Model):
    loop = models.ForeignKey(Loop, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loops")
    joined_at = models.DateTimeField("加入时间", auto_now_add=True)
    is_banned = models.BooleanField("是否被禁", default=False)
    role = models.CharField("角色", max_length=20, choices=[('member', '成员'), ('admin', '管理员')], default='member')  # 新增角色字段

    class Meta:
        unique_together = ("loop", "user")

    def __str__(self):
        return f"{self.user.username} in {self.loop.name}"


class Post(models.Model):
    title = models.CharField("标题", max_length=200, null=False)
    content = models.TextField("内容", null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    loop = models.ForeignKey('Loop', on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)
    location = models.CharField("地理位置", max_length=200, null=True, blank=True)
    price_range = models.TextField("均价", max_length=50, null=True, blank=True)
    image = models.ImageField("图片", upload_to='backer_logs/', null=True, blank=True)
    cuisine = models.CharField("菜系", max_length=100, null=True, blank=True)
    rating = models.FloatField("评分", null=True, blank=True, default=0)  # 新增评分字段

    def __str__(self):
        return self.title


class PostInteraction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="interactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interactions")
    is_liked = models.BooleanField("是否点赞", default=False)
    is_disliked = models.BooleanField("是否点踩", default=False)
    is_favorited = models.BooleanField("是否收藏", default=False)

    class Meta:
        unique_together = ("post", "user")

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField("评论内容", null=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class AdminActionLog(models.Model):
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_actions")
    action = models.CharField("操作", max_length=200)
    target_type = models.CharField("目标类型", max_length=50)  # 比如: User, Post, Comment
    target_id = models.IntegerField("目标ID")
    timestamp = models.DateTimeField("操作时间", auto_now_add=True)

    def __str__(self):
        return f"Admin {self.admin_user.username} performed {self.action} on {self.target_type} ID {self.target_id}"

from django.db import models
from django.utils import timezone
# AA功能
class SplitBill(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_bills")
    amount = models.DecimalField("金额", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    description = models.CharField("账单描述", max_length=255)
    participants = models.ManyToManyField(User, through='SplitBillParticipant')  # 删除 related_name

    def __str__(self):
        return f"Bill by {self.created_by.username} - {self.amount}元"

class SplitBillParticipant(models.Model):
    bill = models.ForeignKey(SplitBill, on_delete=models.CASCADE, related_name="bill_participants")  # 修改 related_name
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participant_in_bills")
    has_paid = models.BooleanField("是否支付", default=False)
    paid_at = models.DateTimeField("支付时间", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} in bill {self.bill.id}"
