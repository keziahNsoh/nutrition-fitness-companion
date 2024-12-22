from django import forms
from .models import Profile, ActivityLog, NutritionLog
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["fitness_goal", "bmi"]


class ActivityLogForm(forms.ModelForm):
    class Meta:
        model = ActivityLog
        fields = ["activity"]


class NutritionLogForm(forms.ModelForm):
    class Meta:
        model = NutritionLog
        fields = ["meal"]
