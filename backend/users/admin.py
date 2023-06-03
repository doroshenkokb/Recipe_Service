from django import forms
from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Follow

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Пользовательская форма создания user
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        verbose_name = 'Пользователь'
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


class FollowAdminForm(forms.ModelForm):
    """
    Кастомная форма для административной панели Follow.
    Проверяет, что подписчик и автор не совпадают.
    """

    class Meta:
        model = Follow
        fields = '__all__'

    def clean(self):
        """
        Проверяет, что подписчик и автор не совпадают.
        Если они совпадают, возбуждает исключение ValidationError.
        """
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        author = cleaned_data.get('author')
        if user == author:
            raise ValidationError("Нельзя подписаться на самого себя")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Follow.
    """
    form = FollowAdminForm
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    autocomplete_fields = ('user', 'author')
