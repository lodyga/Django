from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .models import Item, Category
from .forms import NewItemForm, EditItemForm

def detail_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:3]
    context = {
        "item": item,
        "related_items": related_items}
    return render(request, "item/item_detail.html", context)

def items_view(request):
    query = request.GET.get("query", "")
    categories = Category.objects.all()
    category_id = request.GET.get("category", 0)
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        "items": items,
        "query": query,
        "categories": categories,
        "category_id": int(category_id),
        }
    return render(request, "item/item_browse.html", context)

@login_required
def new_view(request):
    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect("item:detail-view", pk=item.id)
    else:
        form = NewItemForm()
    
    context = {
        "form": form,
        "title": "New item",
        }
    return render(request, "item/item_form.html", context)


@login_required
def delete_view(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    # context = {"item": item}
    # if request.method == "POST":
    item.delete()
    # return render(request, "dashboard/delete_view.html", context)
    return redirect("dashboard:index-view")


@login_required
def edit_view(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == "POST":
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("item:detail-view", pk=item.id)
    else:
        form = EditItemForm(instance=item)
    context = {
        "form": form,
        "title": "Edit item",
        }
    return render(request, "item/item_form.html", context)
