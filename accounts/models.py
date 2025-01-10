from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other")]

    FITNESS_GOALS = [
        ("weight_loss", "Weight Loss"),
        ("muscle_gain", "Muscle Gain"),
        ("maintenance", "Body Maintenance"),
        ("diebetic", "Diet Supervision"),
    ]

    email = models.EmailField(_("email address"), unique=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True
    )
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    fitness_goal = models.CharField(
        max_length=20, choices=FITNESS_GOALS, null=True, blank=True
    )
    profile_picture = models.ImageField(
        upload_to="profile_pics/", null=True, blank=True
    )

    def calculate_bmi(self):
        """Calculate Body Mass Index"""
        if not self.height or not self.weight:
            return None
        # Convert height to meters if needed
        height_m = self.height / 100 if self.height > 3 else self.height
        return round(self.weight / (height_m ** 2), 2)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account_profile'
    )  # Use related_name to avoid conflict with other Profile models
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
