from django.urls import path

from .views import UsersList

app_name = "api"

urlpatterns = [
    path("users", UsersList.as_view())
]