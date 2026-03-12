from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def register_user(request):
    #post /register/ creates user account and immediately logs them in
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email", "")

        if User.objects.filter(username=username).exists():
            return render(request, "login.html", {"error": "username already taken.", "register": True})

        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user) #immediately logs in after registering
        return redirect("dashboard")

    return render(request, "login.html", {"register": True})

def login_user(request):
    #post login will expect a username and pwd
    #deliberately vague error so you cant tell if username exists
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(request, "login.html", {"error": "invalid credentials."})

    return render(request, "login.html")

@login_required
def logout_user(request):
    #will log user out and redirect to login page
    if request.method == "POST":
        logout(request)
        return redirect("login_user")
    return redirect("dashboard")

@login_required
def user_profile(request):
    #get will return logged in user's profile
    #post will update username or email
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        user.save()
        return render(request, "profile.html", {"success": "profile updated."})

    return render(request, "profile.html")