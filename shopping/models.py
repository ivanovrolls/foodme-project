from django.db import models
from django.contrib.auth.models import User
from recipes.models import Ingredient
from mealplanner.models import MealPlan


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_plan = models.ForeignKey(
        MealPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shopping List ({self.user.username})"


class ShoppingItem(models.Model):
    shopping_list = models.ForeignKey(
        ShoppingList,
        on_delete=models.CASCADE,
        related_name="items"
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20, blank=True)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit}"