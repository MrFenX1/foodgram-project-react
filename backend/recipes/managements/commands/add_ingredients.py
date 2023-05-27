from csv import reader

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Добавляем ингредиенты из файла CSV."""
    def handle(self, *args, **options):
        with open(
                'recipe/data/ingredients.csv', 'r',
                encoding='UTF-8'
        ) as ingredients:
            for i in reader(ingredients):
                if len(i) == 2:
                    Ingredient.objects.get_or_create(
                        name=i[0], measurement_unit=i[1],
                    )
