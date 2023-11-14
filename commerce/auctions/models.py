from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)
    description = models.TextField(blank=True)
    img_url = models.URLField(blank=True)
    price = models.FloatField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    w_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default='True')

    def __str__(self):
        return f"{self.title} offered by {self.seller}: ${self.price}"

class Comment(models.Model):
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Listing, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
            return f"Comment made by {self.writer} at {self.date} "

class Bid(models.Model):
    offer = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="product")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bid for {self.offer} for {self.product} made by {self.bidder}"

class Watchlist(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Listing, blank=True)

    def __str__(self):
        return f"{self.person} interests."
