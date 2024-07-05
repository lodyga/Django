from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from .models import Product
from .forms import ProductForm, RawProductForm


# Create your views here.

def product_create_view(request):
    # print(request.POST) # prints whath inside product_create.html imput form
    # if request.method == "POST":
    #     title = request.POST.get("title")
    #     print(title)
    print(request.content_type)
    form = ProductForm(request.POST or None) # None for rendering an empty form
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        form = ProductForm() # rerender a view
    return render(request, "products/product_create.html", context)

def product_update_view(request, id=id):
    obj = Product.objects.get(id=id)
    form = ProductForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    context = {
        "form": form
    }
    return render(request, "products/product_create.html", context)

def product_list_view(request):
    # queryset = Product.objects.all()  # list of objects
    product_list = Product.objects.all()
    context = {
        # "object_list": product_list
        "product_list": product_list
    }
    return render(request, "products/product_list.html", context)

def product_detail_view(request, id=id):
    obj = Product.objects.get(id=id)
    context = {
        "object": obj
    }
    return render(request, "products/product_detail.html", context)

def product_delete_view(request, id):
    obj = get_object_or_404(Product, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect("../../")
    context = {
        "object": obj
    }
    return render(request, "products/product_delete.html", context)

# def product_create_view(request):
#     form = RawProductForm()
#     if request.method == "POST":
#         form = RawProductForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             Product.objects.create(**form.cleaned_data)
# 
#         else:
#             print(form.errors)
# 
#     context = {
#         "form": form
#     }
#     return render(request, "products/product_create.html", context)

def render_initial_data(request):
    initial_data = {
        "title": "Initial title" # not a placeholder but data in that field
    }
    obj = Product.objects.get(id=1)
    form = ProductForm(request.POST or None, initial=initial_data) # instance=obj blocks saving
    # form = ProductForm(request.POST or None, initial=initial_data, instance=obj)
    if form.is_valid():
        form.save()
        form = ProductForm()
    context = {
        "form": form
    }
    return render(request, "products/product_create.html", context)

def dynamic_lookup_view(request, id):
    # obj = Product.objects.get(id=id) # throws an errof if page does not exist
    obj = get_object_or_404(Product, id=id) # handles error if page does not exist
    # try: # same as abowe with try statement
    #     obj = Product.objects.get(id=id)
    # except Product.DoesNotExist:
    #     raise Http404
    context = {
        "object": obj
    }
    return render(request, "products/product_detail.html", context)
