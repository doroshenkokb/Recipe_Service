from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CustomUserViewSet, IngredientsViewSet, RecipesViewSet,
                       TagsViewSet)

router = DefaultRouter()
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
