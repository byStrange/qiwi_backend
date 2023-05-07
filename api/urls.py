from django.urls import path, include

from rest_framework import routers
from knox import views as knox_views

from .views import RegionsList, Region, RegisterView, UsersList

app_name = "api"

urlpatterns = [
    path("regions/", RegionsList.as_view(), name="all_regions"),
    path("regions/<int:pk>", Region.as_view(), name="region"),
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UsersList.as_view(), name="users"),
    path("auth/", include("knox.urls")),
    path("api/auth/logout", knox_views.LogoutView.as_view(), name="knox_logout"),
]
