from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from item.models import Category, Item
# from item.models import Item


@login_required
def index_view(request):
    # items = Item.objects.filter(category="toys")
    items = Item.objects.filter(created_by=request.user)
    # items = Item.objects.all()
    categories = Category.objects.all()

    context = {
        "items": items,
        "categories": categories
    }

    return render(request, "dashboard/index_view.html", context)

@login_required
def category_view(request, pk):
    items = Item.objects.filter(created_by=request.user, category=pk)
    categories = Category.objects.all()
    missing_category = Category.objects.filter(pk=pk)[0]

    context = {
        "items": items,
        "categories": categories,
        "missing_category": missing_category
    }

    return render(request, "dashboard/category_view.html", context)
