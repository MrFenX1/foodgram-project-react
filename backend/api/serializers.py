from rest_framework import serializers

from recipes.models import Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Получаем тэги"""
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientsSerializer(serializers.ModelSerializer):
    """Получаем ингридиенты"""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
