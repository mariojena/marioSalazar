import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Profile, Post, Comment, Request
from .forms import SetPasswordForm

def index(request):

    user = request.user
    posts = []

    # Get the public posts
    if user.is_authenticated:
        for post in Post.objects.all().order_by("-date").values():
            # Get the profile of the person who posted
            person = post["who_id"]
            who_user = User.objects.values('id','username').filter(id=person).values()
            profile = Profile.objects.filter(person=person)

            # Check wether the post is public or if the user follows the person who posted it
            if post["private"] == False or user in profile.get().followers.all() or user.id == person:

                # If True, then add the post to the posts lists
                posts.append(post)
                # print(post.like.all().values('username')) query for getting the likes

                # Get the profile of the post
                post["profile_photo"] = profile.values("profile_photo")[0]["profile_photo"]
                post["user_id"] = who_user.values("pk")[0]["pk"]
                post["username"] = who_user.values("username")[0]["username"]
                post["like"] = list(Post.objects.get(pk = post["id"]).like.all().values_list("username", flat=True))

                # Get the comments related to the post
                post["comments"] = Comment.objects.filter(post=post["id"]).values().order_by("-date")

                # for comment in comments_post: print(comment.like.values()) Query to check the likes of comments
                for comment in post["comments"]:
                    comment["profile_photo"] = Profile.objects.filter(person = comment["writer_id"]).values("profile_photo")[0]["profile_photo"]
                    comment["user_id"] = User.objects.filter(pk = comment["writer_id"]).values("pk")[0]["pk"]
                    comment["username"] = User.objects.filter(pk = comment["writer_id"]).values("username")[0]["username"]
                    comment["like"] = list(Comment.objects.get(pk = comment["id"]).like.all().values_list("username", flat=True))

        # Paginate the posts
        pag_main = Paginator(posts, 10)
        pag_number = request.GET.get('page')
        posts_page = pag_main.get_page(pag_number)
        context = {
            "posts":posts,
            "posts_page": posts_page,
            "profile": Profile.objects.filter(person = user).values("profile_photo")[0]
        }

    else:
        for post in Post.objects.all().filter(private=False).order_by("-date").values():
            posts.append(post)

            person = post["who_id"]
            who_user = User.objects.values('id','username').filter(id=person).values()
            profile = Profile.objects.filter(person=person)

            post["profile_photo"] = profile.values("profile_photo")[0]["profile_photo"]
            post["user_id"] = who_user.values("pk")[0]["pk"]
            post["username"] = who_user.values("username")[0]["username"]
            post["like"] = list(Post.objects.get(pk = post["id"]).like.all().values_list("username", flat=True))


            post["comments"] = Comment.objects.filter(post=post["id"]).values().order_by("-date")

            for comment in post["comments"]:
                comment["profile_photo"] = Profile.objects.filter(person = comment["writer_id"]).values("profile_photo")[0]["profile_photo"]
                comment["user_id"] = User.objects.filter(pk = comment["writer_id"]).values("pk")[0]["pk"]
                comment["username"] = User.objects.filter(pk = comment["writer_id"]).values("username")[0]["username"]
                comment["like"] = list(Comment.objects.get(pk = comment["id"]).like.all().values_list("username", flat=True))

        # Paginate the posts
        pag_main = Paginator(posts, 10)
        pag_number = request.GET.get('page')
        posts_page = pag_main.get_page(pag_number)
        context = {
            "posts":posts,
            "posts_page": posts_page,
        }

    return render(request, "network/index.html", context)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            Profile.objects.create(person=user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def add_post(request):

    if request.method == 'POST':
        # Get the content of the post
        who = request.user
        location = request.POST["location"]
        img_url = request.POST["img_url"]
        description = request.POST["description"]
        # private = [False, True][request.POST["private"] == "on"]
        if request.POST.get("private", True):
            private=True
        else:
            private=False

        post = Post(
            location = location,
            img_url = img_url,
            description = description,
            private = private,
            who = who
        )
        post.save()
        return HttpResponseRedirect(reverse("index"))


def page_user(request, id):
    user_page = User.objects.filter(pk=id).all()[0]
    user = request.user
    posts = []
    profile_page = Profile.objects.filter(person = user_page).values()[0]
    profile_page["followers"] = Profile.objects.get(person = user_page).followers.all()
    # Get if the user is following or not the page
    try:
        profile_page["petition"] = Request.objects.filter(from_user=user.id, to_user= id).values()[0]
    except:
        profile_page["petition"] = ""

    profile_page["following"] = []
    for petition in Request.objects.filter(from_user=user_page, status=2).values():
        profile_page["following"].append(petition)

    # Get the posts
    if user.is_authenticated:
        for post in Post.objects.filter(who = user_page).order_by("-date").values():
            # Get the profile of the person who posted
            person = post["who_id"]
            who_user = User.objects.values('id','username').filter(id=person).values()
            profile = Profile.objects.filter(person=person)

            # Check wether the post is public or if the user follows the person who posted it
            if post["private"] == False or user in profile.get().followers.all() or user == person:

                # If True, then add the post to the posts lists
                posts.append(post)

                # Get the profile of the post
                post["profile_photo"] = profile.values("profile_photo")[0]["profile_photo"]
                post["user_id"] = who_user.values("pk")[0]["pk"]
                post["username"] = who_user.values("username")[0]["username"]
                post["like"] = list(Post.objects.get(pk = post["id"]).like.all().values_list("username", flat=True))

                # Get the comments related to the post
                post["comments"] = Comment.objects.filter(post=post["id"]).values().order_by("-date")

                # for comment in comments_post: print(comment.like.values()) Query to check the likes of comments
                for comment in post["comments"]:
                    comment["profile_photo"] = Profile.objects.filter(person = comment["writer_id"]).values("profile_photo")[0]["profile_photo"]
                    comment["user_id"] = User.objects.filter(pk = comment["writer_id"]).values("pk")[0]["pk"]
                    comment["username"] = User.objects.filter(pk = comment["writer_id"]).values("username")[0]["username"]
                    comment["like"] = list(Comment.objects.get(pk = comment["id"]).like.all().values_list("username", flat=True))
        context = {
            "posts":posts,
            "profile": Profile.objects.filter(person = user).values("profile_photo")[0],
            "profile_page":profile_page,
            "user_page":user_page
        }

    else:
        for post in Post.objects.all().filter(private=False).order_by("-date").values():
            posts.append(post)

            person = post["who_id"]
            who_user = User.objects.values('id','username').filter(id=person).values()
            profile = Profile.objects.filter(person=person)

            post["profile_photo"] = profile.values("profile_photo")[0]["profile_photo"]
            post["user_id"] = who_user.values("pk")[0]["pk"]
            post["username"] = who_user.values("username")[0]["username"]
            post["like"] = list(Post.objects.get(pk = post["id"]).like.all().values_list("username", flat=True))


            post["comments"] = Comment.objects.filter(post=post["id"]).values().order_by("-date")

            for comment in post["comments"]:
                comment["profile_photo"] = Profile.objects.filter(person = comment["writer_id"]).values("profile_photo")[0]["profile_photo"]
                comment["user_id"] = User.objects.filter(pk = comment["writer_id"]).values("pk")[0]["pk"]
                comment["username"] = User.objects.filter(pk = comment["writer_id"]).values("username")[0]["username"]
                comment["like"] = list(Comment.objects.get(pk = comment["id"]).like.all().values_list("username", flat=True))

        context = {
            "posts":posts,
            "profile_page":profile_page,
            "user_page":user_page
        }

    return render(request, "network/person.html", context)


@csrf_exempt
@login_required
def comment(request):
    user = request.user

    # Commenting must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get the content
    data = json.loads(request.body)
    post_id = data.get("post_id")
    content = data.get("content")
    post = Post.objects.get(pk=post_id)
    comment = Comment(
        content=content,
        post=post,
        writer=user
    )
    comment.save()
    # Get the last comment that the user made in this post
    comment_new = Comment.objects.filter(writer=user, post=post).values().last()
    comment_new["profile_photo"] = Profile.objects.filter(person = comment_new["writer_id"]).values("profile_photo")[0]["profile_photo"]
    comment_new["username"] = User.objects.filter(pk = comment_new["writer_id"]).values("username")[0]["username"]
    return JsonResponse([comment_new], safe=False)

@csrf_exempt
@login_required
def settings(request):

    user_info = User.objects.filter(pk=request.user.id).values()[0]
    profile_info = Profile.objects.filter(person=request.user).values()[0]

    if request.method == 'POST':
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        cover_photo = request.POST["cover_photo"]
        profile_photo = request.POST["profile_photo"]
        email = request.POST["email"]

        try:
            User.objects.filter(pk=request.user.id).update(username=username, first_name=first_name, last_name=last_name, email=email)
            Profile.objects.filter(person=request.user).update(profile_photo=profile_photo, cover_photo=cover_photo)
            user_info = User.objects.filter(pk=request.user.id).values()[0]
            profile_info = Profile.objects.filter(person=request.user).values()[0]
            context = {
                "user_info": user_info,
                "profile_info": profile_info
            }
            return render(request, "network/settings.html", context)
        except:
            context = {
                    "user_info": user_info,
                    "profile_info": profile_info,
                    "message":"it was not posible to update the information, try an username that is not used."
                }
            return render(request, "network/settings.html", context)

    context = {
        "user_info": user_info,
        "profile_info": profile_info
    }
    return render(request, "network/settings.html", context)

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
                return render(request, 'network/password_reset_confirm.html', {'form': form, 'message': "Password not valid"})

    form = SetPasswordForm(user)
    return render(request, 'network/password_reset_confirm.html', {'form': form})

@csrf_exempt
@login_required
def like_post(request):
    user = request.user

    # Commenting must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get the content
    data = json.loads(request.body)
    post_id = data.get("post_id")
    post = Post.objects.get(pk=post_id)

    if user in post.like.all():
        post.like.remove(user.pk)
    else:
        post.like.add(user.pk)
    post_like = list(Post.objects.get(pk = post_id).like.values_list("username", flat=True))
    send = {"likes": post_like, "user": request.user.username}
    return JsonResponse([send], safe=False)

@csrf_exempt
@login_required
def like_comment(request):
    user = request.user

    # Commenting must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get the content
    data = json.loads(request.body)
    comment_id = data.get("comment_id")
    comment = Comment.objects.get(pk=comment_id)

    if user in comment.like.all():
        comment.like.remove(user.pk)
    else:
        comment.like.add(user.pk)
    comment_like = list(Comment.objects.get(pk = comment_id).like.values_list("username", flat=True))
    send = {"likes": comment_like, "user": request.user.username}
    return JsonResponse([send], safe=False)


@login_required
def following(request):
    user = request.user
    posts = []

    # Get the public posts
    for post in Post.objects.all().order_by("-date").values():
        # Get the profile of the person who posted
        person = post["who_id"]
        who_user = User.objects.values('id','username').filter(id=person).values()
        profile = Profile.objects.filter(person=person)

        # Check wether the post is public or if the user follows the person who posted it
        if user in profile.get().followers.all() or user.id == person:

            # If True, then add the post to the posts lists
            posts.append(post)
            # print(post.like.all().values('username')) query for getting the likes

            # Get the profile of the post
            post["profile_photo"] = profile.values("profile_photo")[0]["profile_photo"]
            post["user_id"] = who_user.values("pk")[0]["pk"]
            post["username"] = who_user.values("username")[0]["username"]
            post["like"] = list(Post.objects.get(pk = post["id"]).like.all().values_list("username", flat=True))

            # Get the comments related to the post
            post["comments"] = Comment.objects.filter(post=post["id"]).values().order_by("-date")

            # for comment in comments_post: print(comment.like.values()) Query to check the likes of comments
            for comment in post["comments"]:
                comment["profile_photo"] = Profile.objects.filter(person = comment["writer_id"]).values("profile_photo")[0]["profile_photo"]
                comment["user_id"] = User.objects.filter(pk = comment["writer_id"]).values("pk")[0]["pk"]
                comment["username"] = User.objects.filter(pk = comment["writer_id"]).values("username")[0]["username"]
                comment["like"] = list(Comment.objects.get(pk = comment["id"]).like.all().values_list("username", flat=True))
    context = {
        "posts":posts,
        "profile": Profile.objects.filter(person = user).values("profile_photo")[0]
    }
    return render(request, "network/following.html", context)


@csrf_exempt
@login_required
def edit_getpost(request):
    user = request.user

    # Commenting must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get the content
    data = json.loads(request.body)
    post_id = data.get("post_id")
    post = Post.objects.filter(pk=post_id).values()[0]

    return JsonResponse([post], safe=False)

@csrf_exempt
@login_required
def edit_post(request):
    user = request.user

    # Editing a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get the content
    data = json.loads(request.body)
    post_id = data.get("post_id")
    location = data.get("location")
    img_url = data.get("img_url")
    description = data.get("description")
    private = data.get("private")
    Post.objects.filter(pk=post_id).update(location=location, img_url=img_url, description=description,private=private)
    post = Post.objects.filter(pk=post_id).values()[0]
    return JsonResponse([post], safe=False)

@login_required
def notifications(request):
    requests = []
    user = request.user

    for petition in Request.objects.filter(to_user=user).order_by("-date").values():
        person = petition["from_user_id"]
        who_user = User.objects.values('id','username').filter(id=person).values()
        profile = Profile.objects.filter(person=person).values()

            # post["profile_photo"] = profile.values("profile_photo")[0]["profile_photo"]
        petition["img_user"] = profile.values("profile_photo")[0]["profile_photo"]
        petition["username"] = who_user.values("username")[0]["username"]
        requests.append(petition)
    context = {"requests":requests}
    return render(request, "network/notifications.html", context)


@csrf_exempt
@login_required
def accept_request(request):
    user = request.user

    # Accept a request must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get the content
    data = json.loads(request.body)
    petition_id = data.get("request_id")
    Request.objects.filter(pk=petition_id).update(status=2)
    petition = Request.objects.filter(pk=petition_id).values()[0]
    follower = User.objects.get(pk=petition["from_user_id"])
    Profile.objects.get(person=user.id).followers.add(follower)

    return JsonResponse([petition], safe=False)

@csrf_exempt
@login_required
def delete_request(request):
    user = request.user

    # Delete a request or a follower must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get the content
    data = json.loads(request.body)
    petition_id = data.get("request_id")
    petition = Request.objects.filter(pk=petition_id).values()[0]
    follower = User.objects.get(pk=petition["from_user_id"])
    following = User.objects.get(pk=petition["to_user_id"])
    Profile.objects.get(person=following).followers.remove(follower)
    Request.objects.filter(pk=petition_id).delete()

    return JsonResponse(["does not follow you anymore."], safe=False)


@csrf_exempt
@login_required
def send_request(request):
    user = User.objects.get(pk=request.user.id)

    # Delete a request or a follower must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get the content
    data = json.loads(request.body)
    to_user = data.get("to_user_id")
    to_user = User.objects.get(pk=to_user)
    # Create the request
    new_request = Request(to_user=to_user, from_user=user)
    new_request.save()
    petition = Request.objects.filter(to_user=to_user, from_user=user).values()[0]

    return JsonResponse([petition], safe=False)


@csrf_exempt
@login_required
def delete_element(request):

    # Delete an element or a follower must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    id = data.get("id")
    type = data.get("type")

    if type == "deletepost":
        # Deleting the post
        Post.objects.filter(pk=id).delete()
    else:
        # Delete the comment
        Comment.objects.filter(pk=id).delete()

    # Create a dictionary for the id and type to delete in the HTML
    return JsonResponse([""], safe=False)

@csrf_exempt
@login_required
def search(request):
    query = request.GET["q"]
    result=[]
    for name in User.objects.all().values():
        if query.lower() in name["username"].lower():
            # Get the followers
            name["followers"] = []
            name["followers"] = Profile.objects.get(person=name["id"]).followers.all()
            # Get the following
            name["following"] = []
            for petition in Request.objects.filter(from_user=name["id"], status=2).values():
                name["following"].append(petition)
            # Get the profile and cover photo
            name["profile_photo"] = Profile.objects.get(person=name["id"]).profile_photo
            name["cover_photo"] = Profile.objects.get(person=name["id"]).cover_photo

            result.append(name)

    return render(request, "network/search.html", {"result":result})