from django.urls import path
from . import views

urlpatterns = [
    path("", views.fitness_view, name="dashboard"),
    path("new_exercise/", views.new_exercise, name="new_exercise"),
    # path("workout/history/", views.workout_history, name="workout_history"),
    # path("workout/<int:workout_id>/", views.workout_detail, name="workout_detail"),
    # path("workout/<int:workout_id>/edit/", views.edit_workout, name="edit_workout"),
    # path("goals/", views.set_nutrition_goal, name="set_nutrition_goal"),
]
