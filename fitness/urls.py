from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("workout/log/", views.log_workout, name="log_workout"),
    path("workout/history/", views.workout_history, name="workout_history"),
    path("workout/<int:workout_id>/", views.workout_detail, name="workout_detail"),
    path("workout/<int:workout_id>/edit/", views.edit_workout, name="edit_workout"),
]
