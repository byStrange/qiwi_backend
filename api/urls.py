from django.urls import path

from .views import UsersList, RegionsList, Region

app_name = "api"

urlpatterns = [
    path("regions/", RegionsList.as_view()),
    path('regions/<int:pk>', Region.as_view())
]