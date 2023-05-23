from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin

from .models import Follow, User


@register(User)
class CustomUserAmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')


@register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    autocomplete_fields = ('user', 'author')
