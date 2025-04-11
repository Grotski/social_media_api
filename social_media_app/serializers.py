from social_media_app.models import Post, Profile, Comment, Chat, Friends
from rest_framework import serializers


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "sender", "receiver", "content", "created_at"]


class FriendsListSerializer(serializers.ModelSerializer):
    profile_username = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )
    followed_username = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )
    following_username = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Friends
        fields = [
            "id",
            "profile_username",
            "followed_username",
            "following_username",
            "created_at",
        ]


class CommentListSerializer(serializers.ModelSerializer):
    post_title = serializers.SlugRelatedField(read_only=True, slug_field="title")
    commenter_username = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ["id", "commenter_username", "post_title", "created_at"]


class CommentDetailSerializer(CommentListSerializer):
    post_title = serializers.SlugRelatedField(read_only=True, slug_field="title")
    post_content = serializers.SlugRelatedField(read_only=True, slug_field="content")
    commenter_first_name = serializers.SlugRelatedField(
        read_only=True, slug_field="first_name"
    )
    commenter_last_name = serializers.SlugRelatedField(
        read_only=True, slug_field="last_name"
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "post_title",
            "post_content",
            "content",
            "commenter_first_name",
            "commenter_last_name",
            "created_at",
            "updated_at",
        ]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "profile", "created_at"]


class PostListSerializer(PostSerializer):
    profile_full_name = serializers.SlugRelatedField(
        read_only=True, slug_field="full_name"
    )

    class Meta:
        model = Post
        fields = ["id", "title", "profile_full_name", "ceated_at"]


class PostDetailSerializer(PostSerializer):
    profile_username = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )
    profile_full_name = serializers.SlugRelatedField(
        read_only=True, slug_field="full_name"
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "profile_username",
            "profile_full_name",
            "media",
            "ceated_at",
            "updated_at",
        ]


class PostImageSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ["id", "media"]


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


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "profile_picture"]
