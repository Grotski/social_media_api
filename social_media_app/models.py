from django.db import models
from social_media_api_project import settings


class Friends(models.Model):
    followed = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user"
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="users"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_bith = models.DateField(auto_now_add=True)
    bio = models.TextField(max_length=1000)
    friends = models.ManyToManyField(
        "Friends", blank=True, related_name="profiles"
    )
    posts = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="profiles")
    chats = models.ForeignKey("Chat", on_delete=models.CASCADE, related_name="profiles")

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name}, {self.date_of_bith}, {self.bio}"

    class Meta:
        ordering = ["first_name", "last_name"]
