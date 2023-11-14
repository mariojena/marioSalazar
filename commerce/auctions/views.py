from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ModelForm

# Import the models
from .models import User, Listing, Bid, Comment, Watchlist, Category

# Form for creating a listing
class Formcreate(ModelForm):
    class Meta:
        model = Listing
        exclude = ['w_bidder', 'seller', 'active']

class Formbid(forms.Form):
    price = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bid'}))

class Formcomment(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label="")

def index(request):
    return render(request, "auctions/index.html", {
        "listings":Listing.objects.all().filter(active=True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method=='POST':
        form = Formcreate(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            img_url = form.cleaned_data["img_url"]
            price = form.cleaned_data["price"]
            user = User.objects.get(pk=request.user.id)

            new = Listing(title=title, description=description, category=category, img_url=img_url, price=price, seller=user)
            new.save()
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/create.html", {
                "form":form,
                "message": "Remember to fill all the required fields"
            })
    else:
        print(Formcreate)
        return render(request, "auctions/create.html", {
            "form":Formcreate
        })


def listings(request, id_prod):

    try:
        user = User.objects.get(pk=request.user.id)
    except:
        user = None
    try:
        watchlist = Watchlist.objects.get(person=user)
    except:
        watchlist=None
    listing = Listing.objects.get(pk=id_prod)
    bidlist = Bid.objects.all().filter(product=listing).order_by('-offer')
    countbid= Bid.objects.all().filter(product=listing).count()
    try:
        comments = Comment.objects.all().filter(site=listing).order_by('-date')
    except:
        comments=None
    context={
        "listing":listing,
        "formbid":Formbid,
        "formcomment":Formcomment,
        "bidlist":bidlist,
        "comments":comments,
        "countbid":countbid,
        "watchlist":watchlist
    }

    if request.method == 'POST':
        if 'watchlist' in request.POST:
            if watchlist:
                watchlist.products.add(listing)
                return HttpResponseRedirect(reverse("listings", args=(id_prod,)))
            else:
                newwatch = Watchlist(person=user)
                newwatch.save()
                newwatch.products.add(listing)
                return HttpResponseRedirect(reverse("listings", args=(id_prod,)))

        elif 'remove' in request.POST:
            watchlist = Watchlist.objects.get(person=user)
            watchlist.products.remove(listing)
            return HttpResponseRedirect(reverse("listings", args=(id_prod,)))

        elif 'close' in request.POST:
            print(bidlist.last().bidder)
            listing.w_bidder = bidlist.first().bidder
            listing.active = False
            print(listing.active)
            listing.save()
            return HttpResponseRedirect(reverse("listings", args=(id_prod,)))

        elif 'bid' in request.POST:
            formbid=Formbid(request.POST)
            if formbid.is_valid():
                newoffer=formbid.cleaned_data["price"]

                if bidlist and newoffer > bidlist.first().offer:
                    newbid = Bid(offer=newoffer, bidder=user, product=listing)
                    newbid.save()
                    return HttpResponseRedirect(reverse("listings", args=(id_prod,)))
                elif bidlist and newoffer <= bidlist.first().offer:
                    context["message"]=f"your bid should be greater to {bidlist.first().offer}"
                    return render(request, "auctions/listings.html", context)
                elif not bidlist and newoffer >= listing.price:
                    newbid = Bid(offer=newoffer, bidder=user, product=listing)
                    newbid.save()
                    return HttpResponseRedirect(reverse("listings", args=(id_prod,)))
                elif not bidlist and newoffer < listing.price:
                    context["message"]=f"your bid should be greater or equal to {listing.price}"
                    return render(request, "auctions/listings.html", context)

        elif 'comment' in request.POST:
            formcomment=Formcomment(request.POST)
            if formcomment.is_valid():
                newcomment = formcomment.cleaned_data["content"]
                comment = Comment(content=newcomment, writer=user, site=listing)
                comment.save()
                return HttpResponseRedirect(reverse("listings", args=(id_prod,)))

    else:
        if user == listing.seller and listing.active == False:
            print("seller")
            context["message"]=f", you have already closed this auction."
            return render(request, "auctions/listings.html", context)
        elif user== listing.w_bidder and listing.active == False:
            print("winner")
            context["message"]=f", you have already won this auction."
            return render(request, "auctions/listings.html", context)
        else:
            return render(request, "auctions/listings.html", context)

@login_required
def watchlist(request):
    user = User.objects.get(pk=request.user.id)

    if request.method == 'POST':
        listing = Listing.objects.get(pk=request.POST['remove'])
        watchlist = Watchlist.objects.get(person=user)
        watchlist.products.remove(listing)
        return HttpResponseRedirect(reverse("watchlist"))
    try:
        watchlist = Watchlist.objects.get(person=user)
        return render(request, "auctions/watchlist.html", {
            "listings":watchlist.products.all().filter(active=True)
        })
    except:
        return render(request, "auctions/watchlist.html", {
            "message": "You have not added any product to the watchlist"
        })

def categories(request):
    listcat = Category.objects.all()
    context ={
        "listcat":listcat
    }
    return render(request, "auctions/categories.html", context)

def catego(request, cat):
    category = Category.objects.get(url=cat)
    listings = Listing.objects.all().filter(category=category, active=True)
    print(listings)
    return render(request, "auctions/category.html", {
        "category": category.name,
        "listings":listings
    })

def person(request, id):
    person = User.objects.get(pk=id)
    listing = Listing.objects.all().filter(seller=person)
    return render(request, "auctions/person.html", {
        "listings":listing,
        "person": person
    })