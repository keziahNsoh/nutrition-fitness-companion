from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class FoodCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True)
    calories = models.FloatField(validators=[MinValueValidator(0)])
    protein = models.FloatField(validators=[MinValueValidator(0)])
    carbohydrates = models.FloatField(validators=[MinValueValidator(0)])
    fat = models.FloatField(validators=[MinValueValidator(0)])
    serving_size = models.FloatField(default=100)  # in grams
    serving_unit = models.CharField(max_length=50, default="g")

    def __str__(self):
        return self.name


class MealType(models.Model):
    MEAL_CHOICES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack"),
    ]
    name = models.CharField(max_length=20, choices=MEAL_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class MealLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meal_type = models.ForeignKey(MealType, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    total_calories = models.FloatField(default=0)
    total_protein = models.FloatField(default=0)
    total_carbohydrates = models.FloatField(default=0)
    total_fat = models.FloatField(default=0)

    class Meta:
        unique_together = ["user", "date", "meal_type"]
        ordering = ["-date"]


class MealItem(models.Model):
    meal_log = models.ForeignKey(
        MealLog, related_name="items", on_delete=models.CASCADE
    )
    food_item = models.ForeignKey(FoodItem, on_delete=models.PROTECT)
    quantity = models.FloatField(validators=[MinValueValidator(0.1)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_meal_log_totals()

    def update_meal_log_totals(self):
        meal_log = self.meal_log
        meal_items = MealItem.objects.filter(meal_log=meal_log)

        meal_log.total_calories = sum(
            item.food_item.calories * (item.quantity / item.food_item.serving_size)
            for item in meal_items
        )
        meal_log.total_protein = sum(
            item.food_item.protein * (item.quantity / item.food_item.serving_size)
            for item in meal_items
        )
        meal_log.total_carbohydrates = sum(
            item.food_item.carbohydrates * (item.quantity / item.food_item.serving_size)
            for item in meal_items
        )
        meal_log.total_fat = sum(
            item.food_item.fat * (item.quantity / item.food_item.serving_size)
            for item in meal_items
        )

        meal_log.save()


class NutritionGoal(models.Model):
    GOAL_TYPES = [
        ("weight_loss", "Weight Loss"),
        ("weight_gain", "Weight Gain"),
        ("muscle_gain", "Muscle Gain"),
        ("maintenance", "Weight Maintenance"),
        ("performance", "Athletic Performance"),
    ]

    ACTIVITY_LEVELS = [
        ("sedentary", "Sedentary"),
        ("light", "Light Activity"),
        ("moderate", "Moderate Activity"),
        ("very_active", "Very Active"),
        ("extra_active", "Extra Active"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVELS)
    daily_calorie_target = models.IntegerField()
    protein_target = models.FloatField(help_text="Grams of protein per day")
    carbohydrate_target = models.FloatField(help_text="Grams of carbohydrates per day")
    fat_target = models.FloatField(help_text="Grams of fat per day")
    height = models.FloatField(help_text="Height in centimeters")
    current_weight = models.FloatField(help_text="Current weight in kilograms")
    target_weight = models.FloatField(help_text="Target weight in kilograms")
    age = models.IntegerField()
    gender = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_bmr(self):
        if self.gender == "male":
            return 10 * self.current_weight + 6.25 * self.height - 5 * self.age + 5
        else:
            return 10 * self.current_weight + 6.25 * self.height - 5 * self.age - 161

    def calculate_tdee(self):
        bmr = self.calculate_bmr()
        activity_multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "very_active": 1.725,
            "extra_active": 1.9,
        }
        return bmr * activity_multipliers.get(self.activity_level, 1.2)


class MealPlanItem(models.Model):
    meal_plan = models.ForeignKey(
        "MealPlan", related_name="items", on_delete=models.CASCADE
    )
    food_item = models.ForeignKey(FoodItem, on_delete=models.PROTECT)
    quantity = models.FloatField(validators=[MinValueValidator(0.1)])

    def __str__(self):
        return f"{self.food_item.name} ({self.quantity})"


class MealPlan(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    meal_type = models.ForeignKey(MealType, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
