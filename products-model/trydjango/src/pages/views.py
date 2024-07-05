from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home_view(request, *args, **kwargs):
    print(request.user)
    print(args)
    print(kwargs)
    return render(request, "pages/home.html", {})


def contact_view(request, *args, **kwargs):
    return render(request, "pages/contact.html", {"key": "val"})


def about_view(request, *args, **kwargs):
    my_context = {
        "my_text": "This is about me",
        "this_is_true": True,
        "my_number": 123,
        "my_list": ["Ala", "ma", 1, "kota"],
        "my_html": "<h1>hello world</h1>",
    }
    return render(request, "pages/about.html", my_context)


def social_view(request, *args, **kwargs):
    return HttpResponse("<h1>Social Page</h1>")
