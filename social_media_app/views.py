from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .mixins import UploadImageMixin

from .models import Profile, Post, Comment, Chat, Friends

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
    ChatListSerializer,
    FriendsListSerializer,
)

from .permissions import IsAdminOrIfAuthenticatedReadOnly


class FriendsViewSet(viewsets.ModelViewSet):
    queryset = Friends.objects.all()
    serializer_class = FriendsListSerializer
    permission_classes = [
        IsAdminOrIfAuthenticatedReadOnly,
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return FriendsListSerializer
        return FriendsListSerializer


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
