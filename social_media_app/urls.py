from django.urls import path, include
from social_media_app.routing import websocket_urlpatterns
from . import views
from rest_framework.routers import DefaultRouter

from social_media_app.views import ProfileViewSet, PostViewSet, CommentViewSet, FollowViewSet

router = DefaultRouter()
router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)
router.register("follows", FollowViewSet)
# router.register("chats", ChatViewSet, basename="chats")

urlpatterns = [
    path("chat/<str:recipient_username>/", views.chat_view, name="chat"),
    path("", include(router.urls)),
]


app_name = "social_media_app"
