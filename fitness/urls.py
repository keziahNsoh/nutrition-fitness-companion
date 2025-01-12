from django.urls import path
from . import views

urlpatterns = [
    path('', views.fitness_view, name='fitness'),
    path('new_exercise/', views.new_exercise, name='new_exercise'),
    path('add_category/', views.add_category, name='add_category'),
    path('workout_history/', views.workout_history, name='workout_history'),
    path('workout_detail/', views.workout_detail, name='workout_detail'),
]
