from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from nutrition.models import NutritionGoal, MealPlan
from fitness.models import WorkoutLog, FitnessGoal
from health.models import HealthMetric

# Home view with authentication check
@login_required
def home(request):
    user = request.user

    print('i am loading the home page')

    # Handle case where the user doesn't have a profile
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None  # If profile doesn't exist, set it to None

    context = {
        "user": user,
        "profile": profile,
        "fitness_goal": user.fitness_goal
        or "Not set",  # user.fitness_goal is from CustomUser
        "bmi": user.calculate_bmi()
        or "Not set",  # user.calculate_bmi() is from CustomUser
    }
    return render(request, "home.html", context)


@login_required
def dashboard(request):
    """
    Comprehensive user dashboard showing various health and fitness metrics
    """
    try:
        nutrition_goal = NutritionGoal.objects.get(user=request.user)
        recent_meal_plans = MealPlan.objects.filter(user=request.user).order_by(
            "-date"
        )[:3]
    except NutritionGoal.DoesNotExist:
        nutrition_goal = None
        recent_meal_plans = []

    try:
        fitness_goal = FitnessGoal.objects.get(user=request.user)
        recent_workouts = WorkoutLog.objects.filter(user=request.user).order_by(
            "-date"
        )[:3]
    except FitnessGoal.DoesNotExist:
        fitness_goal = None
        recent_workouts = []

    recent_health_metrics = HealthMetric.objects.filter(user=request.user).order_by(
        "-date"
    )[:1]

    context = {
        "title": "Personal Dashboard",
        "nutrition_goal": nutrition_goal,
        "recent_meal_plans": recent_meal_plans,
        "fitness_goal": fitness_goal,
        "recent_workouts": recent_workouts,
        "recent_health_metrics": recent_health_metrics,
    }

    return render(request, "dashboard.html", context)
