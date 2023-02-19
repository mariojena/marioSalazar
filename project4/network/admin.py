from django.contrib import admin

# Register your models here.
from .models import User, Post, Comment, Profile, Request

# How to display models
class CommentAdmin(admin.ModelAdmin):
    filter_horizontal =("like",)

class PostAdmin(admin.ModelAdmin):
    filter_horizontal =("like",)

class FollowerAdmin(admin.ModelAdmin):
    filter_horizontal =("followers",)

# Display mode models
admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, FollowerAdmin)
admin.site.register(Request)