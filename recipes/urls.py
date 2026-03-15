from django.urls import path
from . import views

#url patterns for all recipe endpoints
#allows users to create/view/update/del recipes
#also to access ingredients/tags/recipe steps

urlpatterns = [

    #get all recipes or create new
    path("recipes/", views.recipe_list, name="recipe_list"),
    
    #add a new recipe
    path("recipes/add/", views.add_recipe, name="add_recipe"),

    #edit recipe details
    path("recipes/<int:recipe_id>/edit/", views.edit_recipe, name="edit_recipe"),

    #get/update/del a specific recipe by ID
    path("recipes/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),

    #create new ingredient
    path("ingredients/add/", views.add_ingredient, name="add_ingredient"),

    #get all
    path("ingredients/", views.ingredient_list, name="ingredient_list"),
    path("tags/", views.tag_list, name="tag_list"),
]