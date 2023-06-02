# Generated by Django 3.2.18 on 2023-06-02 16:26

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='Логин')),
                ('first_name', models.CharField(max_length=150, verbose_name='Имя пользователя')),
                ('last_name', models.CharField(max_length=150, verbose_name='Фамилия пользователя')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('password', models.CharField(max_length=150, verbose_name='Пароль')),
                ('favorite_recipes', models.ManyToManyField(related_name='favorites', to='recipes.Recipe', verbose_name='Избранные рецепты')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('shopping_recipes', models.ManyToManyField(related_name='shoppings', to='recipes.Recipe', verbose_name='Список покупок')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('username',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to='users.customusers', verbose_name='Подписчик')),
                ('user_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='users.customusers', verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
                'ordering': ('user',),
            },
        ),
        migrations.AddField(
            model_name='customusers',
            name='subscribing',
            field=models.ManyToManyField(through='users.Subscribe', to='users.CustomUsers', verbose_name='Подписчики'),
        ),
        migrations.AddField(
            model_name='customusers',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='customusers',
            unique_together={('username', 'email')},
        ),
    ]
