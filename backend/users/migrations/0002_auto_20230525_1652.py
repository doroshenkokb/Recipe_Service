# Generated by Django 3.2.19 on 2023-05-25 13:52

import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ('id',), 'verbose_name': 'подписчик', 'verbose_name_plural': 'подписчики'},
        ),
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_follower',
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=150, verbose_name='Пароль'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique subscribe'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(('user', django.db.models.expressions.F('author')), _negated=True), name='Нельзя подписаться на самого себя'),
        ),
    ]
