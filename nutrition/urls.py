from django.urls import path
from . import views

urlpatterns = [
    path("goals/", views.set_nutrition_goal, name="set_nutrition_goal"),
    path("dashboard/", views.nutrition_dashboard, name="nutrition_dashboard"),
    path("meal-plan/create/", views.create_meal_plan, name="create_meal_plan"),
    path("meal-plan/<int:meal_plan_id>/", views.meal_plan_detail, name="meal_plan_detail"),
    path("meal-plan/<int:meal_plan_id>/add-items/",views.add_meal_plan_items,name="add_meal_plan_items"),
    path('food-database/', views.food_item_database, name='food_item_database'),
    path('meal-plans/', views.meal_plan_list, name='meal_plan_list'),
    path('nutrition-goals/', views.nutrition_goal_list, name='nutrition_goal_list'),
]
