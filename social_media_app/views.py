from django.shortcuts import render
from rest_framework import viewsets

from .models import Profile, Post, Comment, Chat, Friends

from .serializers import (
    ProfileListSerializer,
    ProfileDetailSerializer,
    ProfileImageSerializer,
    PostSerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostImageSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
    ChatListSerializer,
    FriendsListSerializer,
)

from .permissions import IsAdminOrIfAuthenticatedReadOnly


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [
        IsAdminOrIfAuthenticatedReadOnly,
    ]

    def get_queryset(self):
        username_param = self.request.query_params.get("username")
        
        queryset = self.queryset
        
        if username_param:
            queryset = queryset.filter(username=username_param)
        return queryset
    
    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        if self.action == "retrieve":
            return ProfileDetailSerializer
        if self.action == "upload_image":
            return ProfileImageSerializer
        return ProfileDetailSerializer
