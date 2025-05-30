from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, min_length=5)
    password2 = serializers.CharField(write_only=True, label="Confirm password")

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "username", "password", "password2", "is_staff")
        read_only_fields = ("is_staff",)
        extra_kwaargs = {"password": {"write_only": True, "min_length": 5}}

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        if password != password2:
            raise serializers.ValidationError("Passwords do not match")

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("password2")
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data = super().validate(attrs)
        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token
