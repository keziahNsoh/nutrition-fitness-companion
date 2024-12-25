from django import forms
from .models import MealLog, NutritionGoal, MealPlan, FoodItem, MealPlanItem


class MealLogForm(forms.ModelForm):
    class Meta:
        model = MealLog
        fields = ["name", "total_calories"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise forms.ValidationError("This field cannot be empty.")
        return name


class NutritionGoalForm(forms.ModelForm):
    """
    Form for creating and updating nutrition goals
    """

    class Meta:
        model = NutritionGoal
        fields = [
            "goal_type",
            "activity_level",
            "height",
            "current_weight",
            "target_weight",
            "age",
            "gender",
        ]
        widgets = {
            "goal_type": forms.Select(attrs={"class": "form-control"}),
            "activity_level": forms.Select(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "height": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "current_weight": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.1"}
            ),
            "target_weight": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.1"}
            ),
            "age": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        """
        Override save method to calculate additional nutritional targets
        """
        instance = super().save(commit=False)

        # Calculate TDEE and nutritional targets
        tdee = instance.calculate_tdee()

        # Basic nutritional target calculations
        if instance.goal_type == "weight_loss":
            instance.daily_calorie_target = int(tdee * 0.8)  # 20% calorie deficit
        elif instance.goal_type == "weight_gain":
            instance.daily_calorie_target = int(tdee * 1.2)  # 20% calorie surplus
        else:
            instance.daily_calorie_target = int(tdee)

        # Protein targets based on goals
        if instance.goal_type == "muscle_gain":
            instance.protein_target = (
                instance.current_weight * 2.2
            )  # Higher protein for muscle gain
        else:
            instance.protein_target = instance.current_weight * 1.6

        # Carb and fat distribution
        instance.carbohydrate_target = (
            instance.daily_calorie_target * 0.4
        ) / 4  # 40% calories from carbs
        instance.fat_target = (
            instance.daily_calorie_target * 0.3
        ) / 9  # 30% calories from fat

        if commit:
            instance.save()
        return instance


class MealPlanForm(forms.ModelForm):
    """
    Form for creating a meal plan
    """

    class Meta:
        model = MealPlan
        fields = ["name", "date", "meal_type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "meal_type": forms.Select(attrs={"class": "form-control"}),
        }


class MealPlanItemForm(forms.ModelForm):
    """
    Form for adding food items to a meal plan
    """

    food_item = forms.ModelChoiceField(
        queryset=FoodItem.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = MealPlanItem
        fields = ["food_item", "quantity"]
        widgets = {
            "quantity": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.1"}
            )
        }


class FoodItemSearchForm(forms.Form):
    """
    Form for searching food items
    """

    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search food items"}
        ),
    )
    category = forms.ChoiceField(
        required=False,
        choices=[("", "All Categories")]
        + list(FoodItem.objects.values_list("category", "category").distinct()),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

class AddMealPlanItemsForm(forms.Form):
    food_item = forms.ModelChoiceField(
        queryset=FoodItem.objects.all(),
        label="Select a food item to add",
        widget=forms.Select(attrs={'class': 'form-control'})
    )