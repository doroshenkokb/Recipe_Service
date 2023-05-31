from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.recipes import IngredientsViewSet, RecipesViewSet, TagsViewSet
from api.views.users import UsersViewSet

router = DefaultRouter()
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path(
        'users/<int:user_id>/subscribe/',
        UsersViewSet.as_view({
            'post': 'subscribe',
            'delete': 'unsubscribe'
        }),
        name='subscribe'
    ),
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
