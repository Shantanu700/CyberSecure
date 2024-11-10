from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date,timedelta

class Category(models.Model):
    name = models.CharField(max_length=255)

class Data(models.Model):
    title = models.CharField(max_length=255, default="Cyber Attack recently occurred")
    info = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    link = models.CharField(max_length=255)
    date = models.DateField(max_length=50)
    num_likes = models.PositiveIntegerField(default=0)
    num_dislikes = models.PositiveIntegerField(default=0)
    content = models.TextField(max_length=510, null=True)

class packages(models.Model):
    pkg_name = models.CharField(max_length=20)
    pkg_price = models.PositiveIntegerField()

class subscriptions(models.Model):
    scr_user = models.ForeignKey(User,on_delete=models.RESTRICT)
    scr_pkg = models.ForeignKey(packages, on_delete=models.RESTRICT)
    scr_start_date = models.DateField(default=date.today)
    end_date = date.today() + timedelta(days=28)
    scr_end_date = models.DateField(default=end_date)
    is_active = models.BooleanField(default=1)
    
class subscribed_cat(models.Model):
    subscription_id = models.ForeignKey(subscriptions, on_delete=models.RESTRICT)
    subscribed_category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    
class UserLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    post = models.ForeignKey(Data, on_delete=models.SET_NULL,null=True)
    is_like = models.BooleanField(default=True)
    
class Comment(models.Model):
    post = models.ForeignKey(Data, on_delete=models.SET_NULL,null=True, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
