from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model): #label ingredients with tags
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model): #denotes the ingredient itself
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model): #relational definition of a recipe
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to="recipes/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model): #junction table design to avoid redundancy and allow different quantities of ingredients
    #while Ingredient table represents the ingredients themselves, this will represent how each recipe uses an Ingredient objkect
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients"
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_recipes"
    )

    quantity = models.FloatField()
    unit = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.ingredient.name} ({self.recipe.title})"