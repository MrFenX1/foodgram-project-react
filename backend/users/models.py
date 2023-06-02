from django.db import models
from django.contrib.auth.models import AbstractUser

from recipes.models import Recipe


class CustomUsers(AbstractUser):

    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
    )

    first_name = models.CharField(
        'Имя пользователя',
        max_length=150,
    )

    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150,
    )
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True,
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
    )
    subscribing = models.ManyToManyField(
        to='self',
        through='Subscribe',
        symmetrical=False,
        verbose_name='Подписчики',
    )
    favorite_recipes = models.ManyToManyField(
        Recipe,
        verbose_name='Избранные рецепты',
        related_name='favorites',
    )
    shopping_recipes = models.ManyToManyField(
        Recipe,
        verbose_name='Список покупок',
        related_name='shoppings',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        unique_together = ('username', 'email')

    def __str__(self):
        return f'Пользователь {self.username}'


class Subscribe(models.Model):
    """
    Модель подписки.
    """

    user = models.ForeignKey(
        CustomUsers,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscriber',
    )
    user_author = models.ForeignKey(
        CustomUsers,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='author',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'user_author'],
                name='уникальность автора на подписчика',
            ),
        ]

    def __str__(self):
        return f'{self.user} подписался на {self.user_author}'
