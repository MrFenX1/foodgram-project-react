from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import (IngredientInRecipe,
                           Recipe)
from recipes.fields import Base64ImageField
from api.serializers import TagSerializer
from users.serializers import UserSerializer


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения списка ингредиентов в рецепте с указанием
    количества.
    """

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )
    amount = serializers.IntegerField(source='quantity')

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipesSerializers(serializers.ModelSerializer):
    """
    Сериализатор для получения данных о рецептах для выдачи их в списке
    подписок.
    """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Выдача рецептов """
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(many=True,
                                               source='ingredient_recipe')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.favorites.filter(id=request.user.id).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.shoppings.filter(id=request.user.id).exists()

    def to_representation(self, instance):
        self.fields['tags'] = TagSerializer(many=True)
        return super().to_representation(instance)

    def validate(self, data):
        ingredients = data['ingredient_recipe']
        existing_ingredient = {}
        for ingredient in ingredients:
            if ingredient['quantity'] <= 0:
                raise ValidationError(
                    'Количество ингредиента должно быть больше 0'
                )
            if ingredient['ingredient']['id'] in existing_ingredient:
                raise ValidationError(
                    'Повторяющие ингредиенты невозможны'
                )
            existing_ingredient['id'] = True
        if data['cooking_time'] <= 0:
            raise ValidationError(
                'Время готовки должно быть больше нуля'
            )
        tags = data['tags']
        existing_tags = {}
        for tag in tags:
            if tag in existing_tags:
                raise ValidationError(
                    'Повторяющиеся теги недопустимы'
                )
            existing_tags['tag'] = True
        return data

    @staticmethod
    def add_tags(recipe, tags):
        recipe.tags.set(tags)

    @staticmethod
    def add_ingredients(recipe, ingredients):
        IngrInRecipe = []
        for ingredient in ingredients:
            IngrInRecipe.append(
                IngredientInRecipe(
                    ingredient_id=ingredient['ingredient']['id'],
                    recipe=recipe,
                    quantity=ingredient['quantity'])
            )
        IngredientInRecipe.objects.bulk_create(IngrInRecipe)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_recipe')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.add_tags(recipe, tags)
        self.add_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.add(*tags)
        ingredients = validated_data.pop('ingredient_recipe')
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        self.add_ingredients(instance, ingredients)
        super().update(instance, validated_data)
        return instance

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]


class UserLikeRecipeSerializer(serializers.ModelSerializer):
    """Избранные рецепты"""
    class Meta:
        model = Recipe
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time'
                  )
