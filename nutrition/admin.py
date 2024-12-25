from django.contrib import admin
from .models import FoodCategory, FoodItem, MealType, MealLog, MealItem, MealPlan, MealPlanItem, NutritionGoal

admin.site.register(FoodCategory)
admin.site.register(FoodItem)
admin.site.register(MealType)
admin.site.register(MealLog)
admin.site.register(MealItem)
admin.site.register(MealPlan)
admin.site.register(MealPlanItem)
admin.site.register(NutritionGoal)
