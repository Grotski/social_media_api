from social_media_app.models import Post, Profile, Comment, Chat, Friends
from rest_framework import serializers


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "sender", "receiver", "content", "created_at"]


class FriendsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ["id", "profile", "followed", "following", "created_at"]


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "commenter", "created_at"]


class CommentDetailSerializer(CommentListSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "content", "commenter", "created_at", "updated_at"]


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "profile"]


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "first_name", "last_name"]


class ProfileDetailSerializer(ProfileListSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "date_of_birth",
            "bio",
            "profile_picture",
        ]
