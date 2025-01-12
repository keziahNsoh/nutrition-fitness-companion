from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
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

@login_required
def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    return render(request, 'exercise_detail.html', {'exercise': exercise})

@login_required
def update_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exercise updated successfully.')
            return redirect('exercise_detail', exercise_id=exercise.id)
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'new_exercise.html', {'form': form, 'exercise': exercise})

@login_required
def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        exercise.delete()
        messages.success(request, 'Exercise deleted successfully.')
        return redirect('fitness')
    return render(request, 'delete_exercise.html', {'exercise': exercise})

