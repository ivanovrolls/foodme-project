from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - Week of {self.week_start}"


class MealPlanDay(models.Model):
    meal_plan = models.ForeignKey(
        MealPlan,
        on_delete=models.CASCADE,
        related_name="days"
    )
    date = models.DateField()
    def __str__(self):
        return f"{self.meal_plan} - {self.date}"

class MealPlanEntry(models.Model):
    MEAL_CHOICES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
    ]
    day = models.ForeignKey(
        MealPlanDay,
        on_delete=models.CASCADE,
        related_name="entries"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES, default="dinner")
    def __str__(self):
        return f"{self.recipe.title} on {self.day.date}"