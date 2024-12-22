from django.contrib import admin
from django.urls import path, include
from core.views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("accounts.urls")),
    path("nutrition/", include("nutrition.urls")),
    path("dashboard/", dashboard, name="dashboard"),
]
