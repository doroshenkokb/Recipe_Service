from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.users.views import SubscribeListView, UsersViewSet

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path(
        "users/subscriptions/",
        SubscribeListView.as_view(),
        name="subscriptions"
    ),
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
