from django.conf import settings
from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin

from .models import Follow, User


@register(User)
class CustomUserAmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')


@register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = ('user', 'author')
