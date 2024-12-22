from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class ExerciseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    DIFFICULTY_LEVELS = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(ExerciseCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    calories_burned_per_hour = models.FloatField(validators=[MinValueValidator(0)])
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    muscle_groups = models.ManyToManyField("MuscleGroup")

    def __str__(self):
        return self.name


class MuscleGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class WorkoutLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    duration = models.FloatField(help_text="Duration in minutes")
    total_calories_burned = models.FloatField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]


class WorkoutExercise(models.Model):
    workout_log = models.ForeignKey(
        WorkoutLog, related_name="exercises", on_delete=models.CASCADE
    )
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    sets = models.IntegerField(validators=[MinValueValidator(1)])
    reps = models.IntegerField(validators=[MinValueValidator(1)])
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")

    def calculate_calories_burned(self):
        # Simple calorie calculation based on exercise and duration
        return self.exercise.calories_burned_per_hour * (self.sets * self.reps / 60)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Update workout log total calories
        self.workout_log.total_calories_burned = sum(
            exercise.calculate_calories_burned()
            for exercise in self.workout_log.exercises.all()
        )
        self.workout_log.save()
