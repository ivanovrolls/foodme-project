from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

def login_view(request):
    return render(request, 'login.html')

def recipes(request):
    return render(request, 'recipes.html')

def meal_planner(request):
    # 暂时用一个简单的占位模板，或者先渲染回 dashboard 防报错
    return render(request, 'meal_planner.html')

def shopping_list(request):
    return render(request, 'shopping_list.html')

def analytics(request):
    return render(request, 'analytics.html')

def profile(request):
    return render(request, 'profile.html')

def recipe_detail(request):
    return render(request, 'recipe_detail.html')

def add_recipe(request):
    return render(request, 'add_recipe.html')