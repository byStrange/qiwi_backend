from django.urls import path, include


from .views import (
    RegionsList,
    Region,
    RegisterView,
    UsersList,
    UserDetailView,
    PostView,
    PostDetailView,
    PostLikeView,
    PostViewView,
    LoginView,
    CategoriesView,
    CheckAuthView,
    ProfileView,
    ADsList,
    GenerateImages,
    ThreadView,
    ThreadChatMessagesAPIView,
    GenerateLocation,
    DeleteMessagesView,
    ReadMessagesView,
)

app_name = "api"

urlpatterns = [
    # test urls
    path("regions/", RegionsList.as_view(), name="all_regions"),
    path("regions/<int:pk>", Region.as_view(), name="region"),
    path("users/", UsersList.as_view(), name="users"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("profile/", ProfileView.as_view(), name="get_user"),
    path("ads/", ADsList.as_view(), name="ads"),
    path("generate-images/", GenerateImages.as_view(), name="generate_images"),
    path("generate-location/", GenerateLocation.as_view(), name="generate_location"),
    path("threads/", ThreadView.as_view(), name="thread"),
    path(
        "threads/<uuid:uuid>/",
        ThreadChatMessagesAPIView.as_view(),
        name="chat_messages",
    ),
    path("delete-messages/", DeleteMessagesView.as_view(), name="delete_messages"),
    path("read-messages/", ReadMessagesView.as_view(), name="read_messages"),
    #  registration
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("check-auth/", CheckAuthView.as_view(), name="check_auth"),
    # main urls
    path("posts/", PostView.as_view(), name="posts"),
    path("posts/<int:pk>", PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/like", PostLikeView.as_view(), name="post_like"),
    path("posts/<int:pk>/view", PostViewView.as_view(), name="post_view"),
    path("categories/", CategoriesView.as_view(), name="categories_view"),
    # knox urls
    path("auth/", include("knox.urls")),
]
