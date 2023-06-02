from django.urls import path, include

from rest_framework import routers

from api.views import TagsViewsSet, IngredientsViewsSet
from users.views import UserViewsSet, GetTokenView, DeleteTokenViews
from recipes.views import RecipeViewset


router = routers.DefaultRouter()
router.register('tags', TagsViewsSet, basename='tag')
router.register('ingredients', IngredientsViewsSet, basename='ingredient')
router.register('users', UserViewsSet, basename='user')
router.register('recipes', RecipeViewset, basename='recipe')


urlpatterns = [
    path('auth/token/login/', GetTokenView.as_view()),
    path('auth/token/logout/', DeleteTokenViews.as_view()),
    path('', include(router.urls))
]
