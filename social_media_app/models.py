import pathlib
import uuid

from django.db import models
from social_media_api_project import settings


class Chat(models.Model):
    sender = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="chats_sent"
    )
    receiver = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="chats_received"
    )
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)


def image_path(instance, filename: str):
    filename = f"{instance.id}-{uuid.uuid4()}" + pathlib.Path(filename).suffix
    return pathlib.Path("uploads/media") / pathlib.Path(filename)


class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=1000)
    commenter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content}"


class Post(models.Model):
    title = models.CharField(max_length=100)
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField(max_length=1000)
    media = models.ImageField(null=True, upload_to=image_path)
    ceated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}: {self.content}"

    class Meta:
        ordering = ["title"]


class Friends(models.Model):
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="friends"
    )
    followed = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="followers"
    )
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="followings"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_bith = models.DateField(auto_now_add=True)
    bio = models.TextField(max_length=1000)
    profile_picture = models.ImageField(null=True, upload_to=image_path)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name}, {self.date_of_bith}, {self.bio}"

    class Meta:
        ordering = ["first_name", "last_name"]
