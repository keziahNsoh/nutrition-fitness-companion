from django.contrib import admin
from .models import FoodCategory, FoodItem, MealType, MealLog, MealItem

admin.site.register(FoodCategory)
admin.site.register(FoodItem)
admin.site.register(MealType)
admin.site.register(MealLog)
admin.site.register(MealItem)
