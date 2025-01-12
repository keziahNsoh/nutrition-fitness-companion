from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from fitness.forms import ExerciseCategoryForm, ExerciseForm
from fitness.models import Exercise, ExerciseCategory


@login_required
def fitness_view(request):
    user = request.user
    exercises = Exercise.objects.all()
    context = {
        "fitness_goal": user.fitness_goal,
        "exercises": exercises,
        "bmi": user.calculate_bmi(),
        "recent_nutrition_logs": [],  # Placeholder for nutrition logs
        "recent_workouts": [],  # Placeholder for workout logs
    }
    return render(request, "fitness.html", context)

@login_required
def new_exercise(request):
    if request.method == 'POST':
        exercise_form = ExerciseForm(request.POST)
        # category_form = ExerciseCategoryForm(request.POST)
        if exercise_form.is_valid():
            exercise = exercise_form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            return redirect('fitness')
    else:
        exercise_form = ExerciseForm()
        category_form = ExerciseCategoryForm()

    return render(request, 'new_exercise.html', {
        'form': exercise_form,
        'category_form': category_form
    })

@login_required
def add_category(request):
    if request.method == 'POST':
        category_form = ExerciseCategoryForm(request.POST)
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully.')
            return redirect('fitness')
    else:
        category_form = ExerciseCategoryForm()

    return render(request, 'add_category.html', {
        'category_form': category_form
    })

@login_required
def workout_history(request):
    user = request.user
    context = {
        "fitness_goal": user.fitness_goal,
        "bmi": user.calculate_bmi(),
        "recent_nutrition_logs": [],  # Placeholder for nutrition logs
        "recent_workouts": [],  # Placeholder for workout logs
    }
    return render(request, "home.html", context)

@login_required
def workout_detail(request):
    user = request.user
    context = {
        "fitness_goal": user.fitness_goal,
        "bmi": user.calculate_bmi(),
        "recent_nutrition_logs": [],  # Placeholder for nutrition logs
        "recent_workouts": [],  # Placeholder for workout logs
    }
    return render(request, "home.html", context)

