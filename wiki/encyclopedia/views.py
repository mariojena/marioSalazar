from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from django import forms
import random

from . import util

class Formnew(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, entry):
    if request.method == 'POST':
        title = request.POST["entry"]
        description = util.get_entry(title)
        initial_data = {
                'title': title,
                'description': description
            }
        form = Formnew(initial_data)
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": title
        })

    markdowner = Markdown()
    description = util.get_entry(entry)
    if  description == None:
        return render(request, "encyclopedia/error.html", {
            "title": entry,
            "error": 2
        })
    else:
        return render(request, "encyclopedia/page.html", {
            "title": entry,
            "description": markdowner.convert(description)
        })

def new(request):
    if request.method == 'POST':
        form = Formnew(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            if util.get_entry(title) == None:
                util.save_entry(title,description)
                return HttpResponseRedirect(f"/wiki/{title}")
            else:
                markdowner = Markdown()
                description = util.get_entry(title)
                return render(request, "encyclopedia/error.html", {
            "title": title,
            "description": markdowner.convert(description),
            "error": 1
        })

    return render(request, "encyclopedia/new.html", {
            "form": Formnew
        })

def edit(request):
    if request.method == 'POST':

        form = Formnew(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            util.save_entry(title,description)
            return HttpResponseRedirect(reverse("index"))

def search(request):
    query = request.GET["q"]
    results=[]
    for title in util.list_entries():
        if query.lower() in title.lower():
            results.append(title)
    if results == []:
        return render(request, "encyclopedia/error.html", {
            "title": query,
            "error": 3
        })
    elif results[0].lower() == query.lower():
        markdowner = Markdown()
        description = util.get_entry(results[0])
        print(description)
        return render(request, "encyclopedia/page.html", {
            "title": results[0],
            "description": markdowner.convert(description)
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "search":query,
            "results":results
        })

def rand(request):
    markdowner = Markdown()
    choice = random.choice(util.list_entries())
    description = util.get_entry(choice)
    return render(request, "encyclopedia/page.html", {
            "title": choice,
            "description": markdowner.convert(description)
        })
