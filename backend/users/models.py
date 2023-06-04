from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=settings.EMAIL
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.FIRST_NAME,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.LAST_NAME,
    )
    password = models.CharField(
        'Пароль',
        max_length=settings.PASSWORD
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user'
            )
        ]

    def __str__(self):
        return (
            f'Пользователь: {self.username}, '
            f'Имя: {self.first_name}, '
            f'Фамилия: {self.last_name}'
        )


class Follow(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Подписчик',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'подписчики'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique subscribe'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='Нельзя подписаться на самого себя',
            ),
        ]

    def __str__(self):
        return (
            f'Подписчик: {self.user.username}, Автор: {self.author.username}'
        )
