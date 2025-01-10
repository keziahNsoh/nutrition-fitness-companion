from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from nutrition.forms import AddMealPlanItemsForm, MealLogForm, MealPlanForm, NutritionGoalForm  # Corrected import
from .models import Profile, MealLog, FoodCategory, FoodItem, NutritionGoal, MealPlan

# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Corrected indentation here
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect(request.GET.get("next", "/"))  # Redirect to the previous page or home
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

@login_required
def homepage(request):
    try:
        nutrition_goal = NutritionGoal.objects.get(user=request.user)
    except NutritionGoal.DoesNotExist:
        nutrition_goal = None
    if request.method == 'POST':
        form = NutritionGoalForm(request.POST)
        # print user
        if form.is_valid():
            nutrition_goal_data = form.cleaned_data
            NutritionGoal.objects.update_or_create(
                user=request.user,
                defaults=nutrition_goal_data
            )
            return redirect('home')  # replace 'success_url' with your success URL
    else:
        form = NutritionGoalForm(instance=nutrition_goal)
    return render(request, 'set_nutrition_goal.html', {'form': form})

# @login_required
# def homepage(request):
#     # Check if the user has a profile
#     try:
#         profile = Profile.objects.get(user=request.user)
#     except Profile.DoesNotExist:
#         profile = None

#     # Fetch the user's meal logs
#     meal_logs = MealLog.objects.filter(user=request.user).order_by('-date')[:5]

#     # Pass context data to the template
#     context = {
#         'meal_logs': meal_logs,
#         'fitness_goal': profile.fitness_goal if profile and profile.fitness_goal else 'Not set yet',
#         'bmi': profile.bmi if profile and profile.bmi else 'Not set yet',
#     }

#     return render(request, 'set_nutrition_goal.html', context)

# View to display all food categories
def food_categories(request):
    categories = FoodCategory.objects.all()
    return render(request, "nutrition/food_categories.html", {"categories": categories})

# View to display food items for a specific category
def food_items_in_category(request, category_id):
    try:
        category = get_object_or_404(FoodCategory, id=category_id)
        food_items = FoodItem.objects.filter(category=category)
    except FoodCategory.DoesNotExist:
        messages.error(request, "Category does not exist.")
        return redirect("nutrition:food_categories")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("nutrition:food_categories")
    return render(
        request,
        "nutrition/food_items_in_category.html",
        {"category": category, "food_items": food_items},
    )

def food_item_database(request):
    # Get all food items from the database
    food_items = FoodItem.objects.all()
    
    # Render the view and pass the food items to the template
    return render(request, 'nutrition/food_item_database.html', {'food_items': food_items})    

# View to add a meal log
@login_required
def add_meal_log(request):
    if request.method == "POST":
        form = MealLogForm(request.POST)
        if form.is_valid():
            meal_log = form.save(commit=False)
            meal_log.user = request.user
            meal_log.save()
            messages.success(request, "Meal log added successfully!")
            return redirect("nutrition:meal_log_list")  # Redirect to the list of meal logs
        else:
            messages.error(request, "Error adding meal log. Please check the form.")
    else:
        form = MealLogForm()
    return render(request, "nutrition/add_meal_log.html", {"form": form})

# View to display a list of meal logs
@login_required
def meal_log_list(request):
    meal_logs = MealLog.objects.filter(user=request.user).select_related('user').order_by("-date")
    # paginator = Paginator(meal_logs, 10)  # Show 10 logs per page
    page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    return render(request, "nutrition/meal_log_list.html", {"page_obj": meal_logs})

# View to set a nutrition goal
@login_required
def set_nutrition_goal(request):
    if request.method == "POST":
        form = NutritionGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, "Nutrition goal set successfully!")
            return redirect("nutrition:nutrition_dashboard")
        else:
            messages.error(request, "Error setting nutrition goal.")
    else:
        form = NutritionGoalForm()
    return render(request, "nutrition/set_nutrition_goal.html", {"form": form})

# View to display the nutrition dashboard
@login_required
def nutrition_dashboard(request):
    user_logs = MealLog.objects.filter(user=request.user)
    total_logs = user_logs.count()
    total_calories = sum(log.total_calories for log in user_logs)
    goal = NutritionGoal.objects.filter(user=request.user).first()

    # Calculate progress toward goal if available
    progress = 0
    if goal:
        progress = (total_calories / goal.daily_calorie_target) * 100 if goal.daily_calorie_target else 0

    return render(request, "nutrition/dashboard.html", {"total_logs": total_logs, "total_calories": total_calories, "progress": progress})

def nutrition_goal_list(request):
    nutrition_goals = NutritionGoal.objects.all()
    return render(request, 'nutrition/nutrition_goal_list.html', {'nutrition_goals': nutrition_goals})

# View to create a meal plan
@login_required
def create_meal_plan(request):
    if request.method == "POST":
        form = MealPlanForm(request.POST)
        if form.is_valid():
            meal_plan = form.save(commit=False)
            meal_plan.user = request.user
            meal_plan.save()
            messages.success(request, "Meal plan created successfully!")
            return redirect("nutrition:meal_plan_list")  # Redirect to the meal plan list
        else:
            messages.error(request, "Error creating meal plan. Please check the form.")
    else:
        form = MealPlanForm()
    return render(request, "nutrition/create_meal_plan.html", {"form": form})

@login_required
def meal_plan_detail(request, meal_plan_id):
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=request.user)
    return render(request, "nutrition/meal_plan_detail.html", {"meal_plan": meal_plan})

def meal_plan_list(request):
    meal_plans = MealPlan.objects.all()
    return render(request, 'nutrition/meal_plan_list.html', {'meal_plans': meal_plans})

@login_required
def add_meal_plan_items(request, meal_plan_id):
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=request.user)
    if request.method == "POST":
        form = AddMealPlanItemsForm(request.POST)
        if form.is_valid():
            food_item = form.cleaned_data['food_item']
            meal_plan.items.add(food_item)  # Assuming a ManyToManyField for items in MealPlan
            messages.success(request, "Item added to the meal plan successfully!")
            return redirect('nutrition:meal_plan_detail', meal_plan_id=meal_plan.id)
        else:
            messages.error(request, "There was an error adding the item. Please check the form.")
    else:
        form = AddMealPlanItemsForm()
    return render(request, 'nutrition/add_meal_plan_items.html', {'form': form, 'meal_plan': meal_plan})

# Edit meal log view
@login_required
def edit_meal_log(request, meal_log_id):
    meal_log = get_object_or_404(MealLog, id=meal_log_id, user=request.user)
    if request.method == "POST":
        form = MealLogForm(request.POST, instance=meal_log)
        if form.is_valid():
            form.save()
            messages.success(request, "Meal log updated successfully!")
            return redirect('nutrition:meal_log_list')
        else:
            messages.error(request, "Error updating meal log.")
    else:
        form = MealLogForm(instance=meal_log)
    return render(request, "nutrition/edit_meal_log.html", {"form": form})

# Edit meal plan view
@login_required
def edit_meal_plan(request, meal_plan_id):
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=request.user)
    if request.method == "POST":
        form = MealPlanForm(request.POST, instance=meal_plan)
        if form.is_valid():
            form.save()
            messages.success(request, "Meal plan updated successfully!")
            return redirect('nutrition:meal_plan_list')
        else:
            messages.error(request, "Error updating meal plan.")
    else:
        form = MealPlanForm(instance=meal_plan)
    return render(request, "nutrition/edit_meal_plan.html", {"form": form})

# User profile page
@login_required
def user_profile(request):
    user_profile = request.user.profile  # Assuming you have a related profile model
    return render(request, "users/profile.html", {"profile": user_profile})

