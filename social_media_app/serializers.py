from social_media_app.models import Post, Profile, Comment, Message, Follow
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "content", "created_at"]


class FollowListSerializer(serializers.ModelSerializer):
    follower_username = serializers.SlugRelatedField(
        read_only=True, slug_field="user__username"
    )
    following_username = serializers.SlugRelatedField(
        read_only=True, slug_field="user__username"
    )

    class Meta:
        model = Follow
        fields = [
            "id",
            "follower_username",
            "following_username",
            "created_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "content"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        validated_data["commenter"] = self.context["request"].user
        return Comment.objects.create(**validated_data)


class CommentListSerializer(serializers.ModelSerializer):
    post_title = serializers.SlugRelatedField(read_only=True, slug_field="title")
    commenter_username = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ["id", "commenter_username", "post_title", "created_at"]


class CommentDetailSerializer(CommentListSerializer):
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
    total_likes = serializers.IntegerField(source="total_likes", read_only=True)
    liked_by_user = serializers.SerializerMethodField()

    def get_liked_by_user(self, obj):
        user = self.context["request"].user
        return obj.likes.filter(pk=user.pk).exists()

    class Meta:
        model = Post
        fields = ["id", "title", "content", "created_at"]


class PostListSerializer(PostSerializer):
    profile_full_name = serializers.SlugRelatedField(
        read_only=True, slug_field="full_name"
    )

    class Meta:
        model = Post
        fields = ["id", "title", "profile_full_name", "media"]


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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "first_name", "last_name"]


class ProfileListSerializer(ProfileSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "profile_picture",
            "first_name",
            "last_name",
            "date_of_birth",
            "bio",
        ]


class ProfileDetailSerializer(ProfileSerializer):
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
