from django.shortcuts import render, redirect
from item.models import Category, Item
from .forms import SignupForm

def index_view(request):
    items = Item.objects.filter(is_sold=False)[:6]
    categories = Category.objects.all()
    context = {
        "items": items,
        "categories": categories
    }
    return render(request, "core/core_index.html", context)

def contact_view(request):
    return render(request, "core/core_contact.html")

def signup_view(request):
    form = SignupForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        return redirect("/login/")

    # if request.method == "POST":
    #     form = SignupForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("/login/")
    # else:
    #     form = SignupForm()

    return render(request, "core/core_signup.html", context)