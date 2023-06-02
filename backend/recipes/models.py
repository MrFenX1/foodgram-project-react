from django.conf import settings
from django.core import validators
from django.db import models


class Ingredient(models.Model):
    """Модель для хранения ингридиентов."""
    name = models.CharField(
        'Название ингредиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        'Единица измерения ингредиента',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='уникальность имени и ед. измерения',
            ),
        ]

    def __str__(self):
        return f'{self.name} ед. измерения {self.measurement_unit}'


class Tag(models.Model):
    """Модель для описания тега."""
    name = models.CharField(
        'Название тега',
        max_length=200,
        unique=True,
        error_messages={
            'unique': 'Указанное имя тега уже существует.',
        },
    )
    color = models.CharField(
        'Цвет в кодировке HEX',
        max_length=7,
        default='#FFDB8B',
        validators=[
            validators.RegexValidator(
                regex=r'#[0-9A-Fa-f]{6}',
                message='Цвет не соответствует HEX кодировке.'
            )
        ]
    )
    slug = models.SlugField(
        'Слаг тега',
        max_length=200,
        unique=True,
        error_messages={
            'unique': 'Указанный слаг уже существует.',
        },
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)


    def __str__(self):
        return f'Тег {self.name}, цвет кода HEX - {self.color}'


class Recipe(models.Model):
    """Модель описания рецепта"""
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        unique=True,
        error_messages={
            'unique': 'Рецепт уже существует.',
        }
    )
    text = models.TextField(
        'Описание рецепта',
    )
    pub_date = models.DateTimeField(
        'Дата создания рецепта',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        validators=[
            validators.MinValueValidator(
                1,
                message='Время должэно быть более 1-ой минуты'
            )
        ]
    )
    image = models.ImageField(
        'Изображение для рецепта',
        upload_to='images/recipe/',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги рецепта',
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиент с количеством для проиготовления рецепта',
        related_name='recipes',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name',)

    def __str__(self):
        return f'Рецепт: {self.name}. автор: {self.author}.'


class IngredientInRecipe(models.Model):
    """Модель связи ингридиента и колличества с конкрктным рецептом"""
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredient_recipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Название рецепта',
        on_delete=models.CASCADE,
        related_name='ingredient_recipe'
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество ингредиента',
        validators=[
            validators.MinValueValidator(
                0,
                message='Ингредиента не может быть 0.'
            )
        ],
    )

    class Meta:
        verbose_name = 'Ингридиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'
        ordering = ('-recipe',)

    def __str__(self):
        return (f'Для {self.recipe} понадобится {self.quantity} '
                f'{self.ingredient}')
