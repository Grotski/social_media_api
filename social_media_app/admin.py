from django.contrib import admin
from social_media_app.models import *


@admin.registe(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "date_of_birth", "bio"]
    search_fields = ["first_name", "last_name"]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "profile", "content", "ceated_at", "updated_at"]
    search_fields = ["title", "content"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "content", "commenter", "created_at", "updated_at"]
    search_fields = ["post", "content", "commenter"]

admin.site.register(Chat)
admin.site.register(Friends)
