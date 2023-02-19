from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Profile(models.Model):
    person = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name="Followers_person")
    followers = models.ManyToManyField(User, blank=True)
    profile_photo = models.URLField(default="https://www.maxpixel.net/static/photo/1x/User-Pictogram-Icon-Profile-6820232.png")
    cover_photo = models.URLField(default="https://www.publicdomainpictures.net/pictures/130000/nahled/grey-gradient-background-1439642315lMp.jpg")

    def __str__(self):
        return f"{self.person} has {self.followers.count()} followers"


class Post(models.Model):
    description = models.TextField()
    img_url = models.URLField(blank=True)
    who = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    location = models.TextField(blank=True, max_length=50)
    like = models.ManyToManyField(User, blank=True, related_name="post_likes")
    private = models.BooleanField(default=False)

    def __str__(self):
        return f"Post made by {self.who}"


class Comment(models.Model):
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_writer")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, blank=True, related_name="comment_likes")

    def __str__(self):
            return f"Comment made by {self.writer} at {self.date}"


class Request(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'Accepted'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"request from {self.from_user} to {self.to_user} is {self.status}"