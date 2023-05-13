from django.urls import path, include

from .views import RegionsList, Region, RegisterView, UsersList, PostView, PostDetailView, PostLikeView, PostViewView, LoginView


app_name = "api"

urlpatterns = [
    # test urls
    path("regions/", RegionsList.as_view(), name="all_regions"),
    path("regions/<int:pk>", Region.as_view(), name="region"),
    path("users/", UsersList.as_view(), name="users"),

    #  registration
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login" ),

    # main urls
    path("posts/", PostView.as_view(), name="posts"),
    path("posts/<int:pk>", PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/like", PostLikeView.as_view(), name="post_like"),
    path("posts/<int:pk>/view", PostViewView.as_view(), name="post_view"),

    # knox urls
    path("auth/", include("knox.urls")),
]
