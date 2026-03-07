from django.contrib import admin
from django.urls import path, include

#root url config for entire project
#connects all applevel url configs

urlpatterns = [
    path("admin/", admin.site.urls),

    #recipes API
    path("api/", include("recipes.urls")),

    #meal planner API
    path("api/", include("mealplanner.urls")),

    #shopping list API
    path("api/", include("shopping.urls")),

    #user/authentication API
    path("api/", include("users.urls")),
]