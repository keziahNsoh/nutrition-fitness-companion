from django.urls import path
from . import views

urlpatterns = [
    # Nutrition Goal URLs
    path("goals/", views.set_nutrition_goal, name="set_nutrition_goal"),
    path("dashboard/", views.nutrition_dashboard, name="nutrition_dashboard"),
    # Meal Plan URLs
    path("meal-plan/create/", views.create_meal_plan, name="create_meal_plan"),
    path(
        "meal-plan/<int:meal_plan_id>/", views.meal_plan_detail, name="meal_plan_detail"
    ),
    path(
        "meal-plan/<int:meal_plan_id>/add-items/",
        views.add_meal_plan_items,
        name="add_meal_plan_items",
    ),
    # Food Item Database
    path("food-database/", views.food_item_database, name="food_item_database"),
]
