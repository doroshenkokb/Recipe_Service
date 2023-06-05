from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.recipes.views import IngredientsViewSet, RecipesViewSet, TagsViewSet

router = DefaultRouter()
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls))
]
