from social_media_app.models import Post, Profile, Comment, Chat, Friends
from rest_framework import serializers

class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "first_name", "last_name"]