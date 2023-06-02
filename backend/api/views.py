from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny

from .serializers import TagSerializer, IngredientsSerializer
from recipes.models import Tag, Ingredient


class TagsViewsSet(ReadOnlyModelViewSet):
    """Получаем теги. Эндпоинт ./tags/<id>/"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class IngredientsViewsSet(ReadOnlyModelViewSet):
    """Получаем теги. Эндпоинт ./ingredients/<id>/"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [AllowAny]
