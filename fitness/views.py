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
    ExerciseCategoryFormSet = inlineformset_factory(
        Exercise, ExerciseCategory, form=ExerciseCategoryForm, extra=1, can_delete=False
    )

    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        formset = ExerciseCategoryFormSet(request.POST, request.FILES)
        # print user
        if form.is_valid() and formset.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            formset.instance = exercise
            formset.save()
            return redirect('fitness')
        else:
            form = ExerciseForm()
            formset = ExerciseCategoryFormSet()
            return render(request, 'new_exercise.html', {'form': form, 'formset': formset})
        
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
