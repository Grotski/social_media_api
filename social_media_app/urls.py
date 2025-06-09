from django.urls import path, include
from rest_framework.routers import DefaultRouter

from social_media_app.views import ProfileViewSet, PostViewSet, CommentViewSet, FollowViewSet, ChatViewSet

router = DefaultRouter()
router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)
router.register("follows", FollowViewSet)
router.register("chats", ChatViewSet, basename="chat")

urlpatterns = [
    path("", include(router.urls)),
]


app_name = "social_media_app"
