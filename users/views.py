from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ActivityLogForm, NutritionLogForm
from .models import Profile, ActivityLog, NutritionLog
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomUserCreationForm

# Register View
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


# Dashboard View
def dashboard_view(request):
    user = request.user
    context = {
        "fitness_goal": user.fitness_goal,
        "bmi": user.calculate_bmi(),
    }
    return render(request, "users/dashboard.html", context)


# Profile View
def profile_view(request):
    pass


# View to update user profile
@login_required
def update_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("home")  # Redirect to home after saving the profile
    else:
        form = ProfileForm(instance=profile)

    return render(request, "update_profile.html", {"form": form})


# View to add activity log
@login_required
def add_activity_log(request):
    if request.method == "POST":
        form = ActivityLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect("home")
    else:
        form = ActivityLogForm()

    return render(request, "add_activity_log.html", {"form": form})


# View to add nutrition log
@login_required
def add_nutrition_log(request):
    if request.method == "POST":
        form = NutritionLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect("home")
    else:
        form = NutritionLogForm()

    return render(request, "add_nutrition_log.html", {"form": form})
