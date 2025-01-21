from django.urls import path
from . import views

urlpatterns = [
    path('', views.fitness_view, name='fitness'),
    path('new_exercise/', views.new_exercise, name='new_exercise'),
    path('add_category/', views.add_category, name='add_category'),
    path('workout_history/', views.workout_history, name='workout_history'),
    path('workout_detail/<int:workout_id>/', views.workout_detail, name='workout_detail'),
    path('exercise/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('exercise/<int:exercise_id>/update/', views.update_exercise, name='update_exercise'),
    path('exercise/<int:exercise_id>/delete/', views.delete_exercise, name='delete_exercise'),
    path('create_workout/', views.create_workout, name='create_workout'),
    path('workout_detail/<int:workout_id>/delete/', views.delete_workout, name='delete_workout'),
]
