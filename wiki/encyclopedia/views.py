from django.shortcuts import render

from . import util
import random
from django.http import HttpResponseRedirect
from django.urls import reverse

import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry = util.get_entry(title)
    if entry is not None:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(util.get_entry(title))
        })
    return render(request, "encyclopedia/entry.html", {
        "title": 'This page does not exist',
        "entry": markdown2.markdown(util.get_entry('NotListedEntries/NullPage'))
    })


def search_result(request):
    query = request.GET["q"]
    entries = util.list_entries()
    if entries.__contains__(query):
        return render(request, "encyclopedia/entry.html", {
            "title": query,
            "entry": util.get_entry(query)
        })
    searchentries = list()
    for entry in entries:
        if entry.__contains__(query):
            searchentries.append(entry)
    return render(request, "encyclopedia/search_result.html", {
        "entries": searchentries
    })


def new_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        entries = util.list_entries()
        if entries.__contains__(title):
            return render(request, "encyclopedia/new_page.html", {
                "message": "This entry already exists, you can edit this entry in the article page!",
            })
        else:
            content = request.POST["ltext"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/new_page.html", {
                "message": "",
            })
    else:
        return render(request, "encyclopedia/new_page.html", {
            "message": "",
        })


def edit_page(request, title):
    if request.method == "POST":
        content = request.POST["ltext"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=(title,)))
    else:
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "entry": markdown2.markdown(util.get_entry(title))
        })


def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", args=(title,)))
