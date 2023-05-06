from django.urls import path

from .views import  RegionsList, Region, SetCityView

app_name = "api"

urlpatterns = [
    path("regions/", RegionsList.as_view(), name="all_regions"),
    path('regions/<int:pk>', Region.as_view(), name="region"),
    path('regions/set', SetCityView.as_view(), name="set_city" )
]