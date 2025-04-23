from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .mixins import UploadImageMixin

from .models import Profile, Post, Comment, Message, Follow

from .serializers import (
    ProfileListSerializer,
    ProfileDetailSerializer,
    ProfileImageSerializer,
    PostSerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostImageSerializer,
    CommentSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
    FollowListSerializer,
)

from .permissions import IsAdminOrIfAuthenticatedReadOnly


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowListSerializer
    permission_classes = [
        IsAdminOrIfAuthenticatedReadOnly,
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return FollowListSerializer
        return FollowListSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsAdminOrIfAuthenticatedReadOnly,
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer
        if self.action == "retrieve":
            return CommentDetailSerializer
        return CommentSerializer


class PostViewSet(UploadImageMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        IsAdminOrIfAuthenticatedReadOnly,
    ]

    def get_queryset(self):
        title_param = self.request.query_params.get("title")
        profile_username = self.request.query_params.get("profile.username")

        queryset = self.queryset

        if title_param:
            queryset = queryset.filter(title=title_param)
        if profile_username:
            queryset = queryset.filter(profile__username=profile_username)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        if self.action == "upload_image":
            return PostImageSerializer
        return PostDetailSerializer

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def toggle_like_unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if post.likes.filter(pk=user.pk).exists():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return Response(status=status.HTTP_200_OK)


class ProfileViewSet(UploadImageMixin, viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [
        IsAdminOrIfAuthenticatedReadOnly,
    ]

    def get_queryset(self):
        username_param = self.request.query_params.get("username")
        first_name_param = self.request.query_params.get("first_name")
        last_name_param = self.request.query_params.get("last_name")

        queryset = self.queryset

        if username_param:
            queryset = queryset.filter(username=username_param)
        if first_name_param:
            queryset = queryset.filter(first_name=first_name_param)
        if last_name_param:
            queryset = queryset.filter(last_name=last_name_param)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        if self.action == "retrieve":
            return ProfileDetailSerializer
        if self.action == "upload_image":
            return ProfileImageSerializer
        return ProfileDetailSerializer

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def toggle_follow_unfollow(self, request, pk=None):
        profile_to_follow = Profile.objects.get(pk=pk)
        follower_profile = request.user.profile

        if profile_to_follow == follower_profile:
            return Response(
                {"status": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if follower_profile.followings.filter(pk=profile_to_follow.pk).exists():
            follower_profile.followings.remove(profile_to_follow)
            status_msg = "unfollowed"
        else:
            follower_profile.followings.add(profile_to_follow)
            status_msg = "followed"
        return Response({"status": status_msg}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def followers(self, request, pk=None):
        profile = self.get_object()
        followers = Follow.objects.filter(follower=profile)
        serializer = FollowListSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def followings(self, request, pk=None):
        profile = self.get_object()
        followings = Follow.objects.filter(following=profile)
        serializer = FollowListSerializer(followings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
