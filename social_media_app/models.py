import pathlib
import uuid

from django.db import models
from social_media_api_project import settings


class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"timestamp: {self.created_at} from {self.sender} to {self.receiver}: {self.content}"


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
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes", blank=True)
    ceated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}: {self.content}"
    
    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ["title"]


class Follow(models.Model):
    follower = models.ForeignKey(
        "Profile", related_name="followers", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        "Profile", related_name="followings", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["follower", "following"]
        ordering = ["-created_at"]
        
    def __str__(self):
        return f"{self.follower} follows {self.following}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(auto_now_add=True)
    bio = models.TextField(max_length=1000)
    profile_picture = models.ImageField(null=True, upload_to=image_path)
    profile_followers = models.ManyToManyField("self", through=Follow, symmetrical=False)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name}, {self.date_of_birth}, {self.bio}"

    class Meta:
        ordering = ["first_name", "last_name"]
