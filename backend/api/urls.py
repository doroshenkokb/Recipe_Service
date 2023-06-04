from django.urls import include, path

urlpatterns = [
    path('', include('recipes.urls')),
    path('', include('users.urls')),
]
