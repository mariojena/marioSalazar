from django.contrib import admin

from .models import User, Listing, Comment, Bid, Watchlist, Category

class WatchlistAdmin(admin.ModelAdmin):
    filter_horizontal =("products",)

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Category)