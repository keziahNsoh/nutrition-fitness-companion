from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Profile
from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib.auth.decorators import login_required

# Home view
@login_required  # This ensures only authenticated users can access this view
def home(request):
    user = request.user

    # Handle case where the user doesn't have a profile
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None  # If profile doesn't exist, set it to None

    context = {
        "user": user,
        "profile": profile,
        "fitness_goal": user.fitness_goal
        or "Not set",  # user.fitness_goal is from CustomUser
        "bmi": user.calculate_bmi()
        or "Not set",  # user.calculate_bmi() is from CustomUser
    }
    return render(request, "home.html", context)


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            messages.success(request, "Registration successful!")  # Success message
            return redirect("home")  # Redirect to home after registration
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        # Check if 'username' and 'password' are in the POST request
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:  # Ensure both fields are provided
            user = authenticate(request, username=username, password=password)
            print("trying to authenticate")
            # log user to console
            print(f"User {user} trying to authenticate")
            if user is not None:
                login(request, user)
                # log to console 
                print(f"User {user} logged in")
                messages.success(request, "Login successful!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Both username and password are required.")

    return render(request, "login.html")


def update_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Profile updated successfully!"
            )  # Success message
            return redirect("home")  # Redirect to home after updating
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "update_profile.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")  # Success message
    return redirect("login")  # Redirect to login after logout
