from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path("chat/<uuid:thread_id>/", consumers.ChatConsumer.as_asgi()),
    path("ws/posts/", consumers.PostConsumer.as_asgi()),
    path("ws/users/", consumers.UserConsumer.as_asgi()),
]
