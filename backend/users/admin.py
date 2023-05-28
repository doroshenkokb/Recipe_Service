from django.contrib.admin import ModelAdmin, register
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import Follow

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Пользовательская форма создания user
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        verbose_name_plural = 'Пользователи'


@register(User)
class CustomUserAdmin(UserAdmin):
    """
    Административная панель для User
    """

    add_form = CustomUserCreationForm
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'


@register(Follow)
class FollowAdmin(ModelAdmin):
    """
    Административная панель Follow
    """

    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    autocomplete_fields = ('user', 'author')
