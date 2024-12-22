from django import forms
from .models import WorkoutSession, Exercise


class WorkoutSessionForm(forms.ModelForm):
    """
    Form for creating and editing workout sessions.
    Allows users to log their complete workout, including exercises.
    """

    class Meta:
        model = WorkoutSession
        fields = ["workout_type", "duration", "total_calories_burned", "date", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class ExerciseForm(forms.ModelForm):
    """
    Form for adding individual exercises to a workout session.
    Supports detailed exercise tracking with sets, reps, and weight.
    """

    class Meta:
        model = Exercise
        fields = [
            "exercise_name",
            "exercise_type",
            "sets",
            "reps",
            "weight",
            "duration",
        ]
        widgets = {
            "exercise_name": forms.TextInput(attrs={"class": "form-control"}),
            "exercise_type": forms.Select(attrs={"class": "form-control"}),
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
