from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserProfileForm


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            messages.success(request, "Registration successful!")
            return redirect(
                "dashboard"
            )  # Redirect to dashboard after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")  # Redirect back to the profile page
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        "form": form,
        "bmi": request.user.calculate_bmi(),  # Calculate BMI to display
    }
    return render(request, "users/profile.html", context)


@login_required
def dashboard_view(request):
    user = request.user
    context = {
        "fitness_goal": user.fitness_goal,
        "bmi": user.calculate_bmi(),
        "recent_nutrition_logs": [],  # Placeholder for nutrition logs
        "recent_workouts": [],  # Placeholder for workout logs
    }
    return render(request, "home.html", context)
