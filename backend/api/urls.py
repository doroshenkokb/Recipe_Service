from django.urls import include, path

urlpatterns = [
    path('', include('api.recipes.urls')),
    path('', include('api.users.urls')),
]
