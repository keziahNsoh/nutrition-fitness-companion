from django import forms

from .models import Exercise, ExerciseCategory, WorkoutExercise

formClass = "bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

class ExerciseCategoryForm(forms.ModelForm):
    """
    Form for adding a new exercise category to the database.
    """

    class Meta:
        model = ExerciseCategory
        fields = ["name", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

class ExerciseForm(forms.ModelForm):
    """
    Form for adding a new exercise to the database.
    """

    class Meta:
        model = Exercise
        fields = [
            "name",
            "category",
            "description",
            "calories_burned_per_hour",
            "difficulty",
            "muscle_groups",
        ]
        widgets = {
            "muscle_groups": forms.CheckboxSelectMultiple(),
            "calories_burned_per_hour": forms.NumberInput(attrs={"step": "0.01", "class": formClass}),
            "difficulty": forms.Select(attrs={"class": formClass}),
            "category": forms.Select(attrs={"class": formClass}),
            "name": forms.TextInput(attrs={"class": formClass}),
            "description": forms.Textarea(attrs={"class": formClass, "rows": 3}),
        }


class WorkoutExerciseForm(forms.ModelForm):
    """
    Form for adding individual exercises to a workout session.
    Supports detailed exercise tracking with sets, reps, and weight.
    """

    class Meta:
        model = WorkoutExercise
        fields = [
            "sets",
            "reps",
            "weight",
        ]
        widgets = {
            "weight": forms.Select(attrs={"class": "form-control"}),
        }


class WorkoutLogForm(forms.Form):
    """
    Comprehensive form for logging a complete workout with multiple exercises.
    Provides a more flexible approach to workout tracking.
    """

    workout_type = forms.ChoiceField(
        choices=[
            ("strength", "Strength Training"),
            ("cardio", "Cardio"),
            ("flexibility", "Flexibility/Yoga"),
            ("other", "Other"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    total_duration = forms.IntegerField(
        label="Total Workout Duration (minutes)",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    calories_burned = forms.IntegerField(
        required=False,
        label="Calories Burned (optional)",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
    )

    # Dynamic exercise fields can be added programmatically if needed
    def add_exercise_fields(self, num_exercises):
        """
        Dynamically add exercise fields to the form.
        Useful for allowing users to log multiple exercises in one form.
        """
        for i in range(num_exercises):
            self.fields[f"exercise_name_{i}"] = forms.CharField(
                label=f"Exercise {i+1} Name",
                required=False,
                widget=forms.TextInput(attrs={"class": "form-control"}),
            )
            self.fields[f"exercise_sets_{i}"] = forms.IntegerField(
                label=f"Sets for Exercise {i+1}",
                required=False,
                widget=forms.NumberInput(attrs={"class": "form-control"}),
            )
