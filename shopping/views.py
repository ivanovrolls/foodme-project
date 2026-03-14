from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ShoppingList, ShoppingItem
from mealplanner.models import MealPlanEntry, MealPlan


@login_required
def shoppinglist_list(request):
    #get/shoppinglists/ will list all shopping lists for logged in user
    #post /shoppinglists/ will create a new shopping list (can autogen items from meal plan)
    #autogen is handled by passing a meal plan id in the request
    if request.method == "POST":
        meal_plan_id = request.POST.get("meal_plan_id")
        meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=request.user) if meal_plan_id else None
        shopping_list = ShoppingList.objects.create(user=request.user, meal_plan=meal_plan)

        #autogen here
        if meal_plan:
            generate_items_from_plan(shopping_list, meal_plan)

        return redirect("shoppinglist_detail", list_id=shopping_list.id)

    lists = ShoppingList.objects.filter(user=request.user).prefetch_related("items")
    meal_plans = MealPlan.objects.filter(user=request.user)
    return render(request, "shopping_list.html", {"lists": lists, "meal_plans": meal_plans})


@login_required
def shoppinglist_detail(request, list_id):
    #get and del
    shopping_list = get_object_or_404(ShoppingList, id=list_id, user=request.user)

    if request.method == "POST" and request.POST.get("_action") == "delete":
        shopping_list.delete()
        return redirect("shoppinglist_list")

    items = shopping_list.items.all()
    return render(request, "shopping_list.html", {"shopping_list": shopping_list, "items": items})


@login_required
def shopping_items(request, list_id):
    #get will list all items in shopping list
    #post will add custom item to shoping list
    shopping_list = get_object_or_404(ShoppingList, id=list_id, user=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        unit = request.POST.get("unit", "")
        ShoppingItem.objects.create(
            shopping_list=shopping_list,
            name=name,
            quantity=quantity,
            unit=unit,
        )
        return redirect("shoppinglist_detail", list_id=shopping_list.id)

    items = shopping_list.items.all()
    return render(request, "shopping_list.html", {"shopping_list": shopping_list, "items": items})


@login_required
def mark_item_purchased(request, item_id):
    #patch to modify, will toggle item purchase status
    #traverse the foreign key to verify this item belongs to the requesting user
    item = get_object_or_404(ShoppingItem, id=item_id, shopping_list__user=request.user)
    if request.method == "POST":
        item.purchased = not item.purchased
        item.save()
    return redirect("shoppinglist_detail", list_id=item.shopping_list.id)


def generate_items_from_plan(shopping_list, meal_plan):
    #fetch every recipe entry in this meal plan across all days
    entries = MealPlanEntry.objects.filter(
        day__meal_plan=meal_plan
    ).select_related("recipe").prefetch_related("recipe__recipe_ingredients__ingredient")

    #aggregate
    aggregated = {}
    for entry in entries:
        for ri in entry.recipe.recipe_ingredients.all():
            key = (ri.ingredient.id, ri.unit)
            if key in aggregated:
                aggregated[key]["quantity"] += ri.quantity
            else:
                aggregated[key] = {
                    "ingredient": ri.ingredient,
                    "name": ri.ingredient.name,
                    "quantity": ri.quantity,
                    "unit": ri.unit,
                }

    #bulk create all items in one DB call
    ShoppingItem.objects.bulk_create([
        ShoppingItem(
            shopping_list=shopping_list,
            ingredient=data["ingredient"],
            name=data["name"],
            quantity=data["quantity"],
            unit=data["unit"],
            purchased=False,
        )
        for data in aggregated.values()
    ])