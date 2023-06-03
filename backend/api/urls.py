from django.urls import include, path

from api.recipes.urls import urlpatterns as recipes_urls
from api.users.urls import urlpatterns as users_urls

urlpatterns = [
    path(r'auth/', include('djoser.urls.authtoken')),
]

urlpatterns += users_urls
urlpatterns += recipes_urls
