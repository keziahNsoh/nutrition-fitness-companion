from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "birth_date",
            "gender",
            "height",
            "weight",
            "fitness_goal",
            "profile_picture",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "birth_date",
            "gender",
            "height",
            "weight",
            "fitness_goal",
            "profile_picture",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "height": forms.NumberInput(attrs={"step": "0.1"}),
            "weight": forms.NumberInput(attrs={"step": "0.1"}),
        }
