from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from .models import FoodCategory
from .forms import MealLogForm
from django.contrib.auth.decorators import login_required

# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


# View to display all food categories
def food_categories(request):
    categories = FoodCategory.objects.all()
    return render(request, "nutrition/food_categories.html", {"categories": categories})


# View to display food items for a specific category
def food_items_in_category(request, category_id):
    category = get_object_or_404(FoodCategory, id=category_id)
    food_items = FoodItem.objects.filter(category=category)
    return render(
        request,
        "nutrition/food_items_in_category.html",
        {"category": category, "food_items": food_items},
    )


# View to add a meal log
@login_required
def add_meal_log(request):
    if request.method == "POST":
        form = MealLogForm(request.POST)
        if form.is_valid():

            form.save()
            return HttpResponseRedirect(
                reverse("nutrition:meal_log_list")
            )  # Redirect to a list of meal logs
    else:
        form = MealLogForm()

    return render(request, "nutrition/add_meal_log.html", {"form": form})


def meal_log_list(request):
    # Fetch meal logs for the logged-in user
    meal_logs = MealLog.objects.filter(user=request.user).order_by("-date")
    return render(request, "nutrition/meal_log_list.html", {"meal_logs": meal_logs})
