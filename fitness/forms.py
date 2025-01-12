from django import forms
from .models import Exercise, WorkoutExercise


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
