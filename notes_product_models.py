"""
Python Django Web Framework - Full Course for Beginners
https://youtu.be/F5mRW0jo-U4?si=Xjjb8j191M5l6OTb
"""

import django
django.get_version()

# 3 - Setup your Virtual Environment for Django
$ virtualenv .  # creates virtualenv here; virtualenv -p python3 .
$ virtualenv my_env  # creates virtualenv in my_env folder
$ virtualenv my_env -p /usr/bin/python3 # uses python from provided path
$ python3 -m venv . # creates virtualenv with python module
$ source bin/activate  # activates virtualenv "bin/activate" = path
$ pip install Django==2.0.7  # install Django
$ deactivete  # deactivates virtualenv
$ which python3  # python working dir

# 4 - Create a Blank Django Project
$ django-admin # subcommands
$ django-admin startproject trydjango .  # in src forder, if errors then install newest version with python -m pip install -U Django
$ python3 manage.py runserver  # starts server
$ http://127.0.0.1:8000/admin

# 6 - Settings
template: html page rendered in Django
BASE_DIR = Path(__name__).resolve().parent.parent  # file path
$ python3 manage.py migrate # migrate sync settings with projects/apps

# 7 - Built-In Components
$ python3 manage.py createsuperuser

# 8 - Your First App Component
$ python3 manage.py startapp <appname>  # create a component/app
# Add created app to settings.py INSTALLED_APPS
# Model fields maps data to the database.
$ python3 manage.py migrate && python3 manage.py makemigrations # run when models.py changes
admin.py: from .models import <app_name>; admin.site.register(<app_name>)

# 9 - Create Product Objects in the Python Shell
$ python3 manage.py shell  # run Django in Python Interpreter (in terminal)
D>>> from products.models import Product
D>>> Product.objects.all() # prints all products objects
D>>> Product.objects.create(title="bash_title", description="bash_descript", price=45, summary="shel_sum") # 
D>>> Product.objects.get(id=1).title

# 10 - New Model Fields
models.CharField()
models.TextField()
models.DecimalField()
models.BooleanField()
$ python3 manage.py makemigrations && python3 manage.py migrate # makes a migration file for a model and sync it with the database 

# 11 - Change a Model
blank = True # refers to a field in a model
null = True # refers to a cell in a database

# 12 - Default Homepage to Custom Homepage
# Create a class of a function based view
# View handles hequst/webpages; HttpRequest -> HttpResponse
from pages.views import home_view
Import a view to work with an URL.

# 13 - URL Routing and Requests
Rout a path to a view.
A view hadles an URL.

# 14 - Django Templates
URL requests -> server/Django returns a response
Break URL and sends a function to respond

# 15 - Django Templating Engine Basics
{{}} Django renders whats inside
Templete inheritance.
extends, block, include

# 16 - Include Template Tag
{% include ".html" %}

# 17 - Rendering Context in a Template
From view pass context to a template.
context + template -> html to browser
context variable: variable passed from view to template in dict format

# 18 - For Loop in a Template
Built-in template tags and filters

# 19 - Using Conditions in a Template

# 20 - Template Tags and Filters
Templet Tags: extends, block, include, for, if
Filter: |add:1

# 21 - Render Data from the Database with a Model
# Load from a Database
D>>> obj = Product.objects.get(id=1) # get product item
D>>> dir(obj)
context = {"object": obj}

# 22 - How Django Templates Load with Apps

# 23 - Django Model Forms
Creating form for a model.
form.as_p: Build-in method turn a passing form as context to htlm form redered ouf with paragraph tags.
form = ProductForm() Rerender a view so context changes to blank.

# 24 - Raw HTML Form
<!--google search-->
<form action="http://www.google.com/search" method="GET">
    <input type="text" name="q" placeholder="Input search">
    <input type="submit" value="Save">
</form>

# 25 - Pure Django Form
print(dir(request))
print(request.headers)
In (forms.Form) as oppose to (forms.ModelForm) there's a need to declare inputs.
Instance from a form like an instance from a class.
POST, GET: types of Requests

# 26 - Form Widgets

# 27 - Form Validation Methods
def clean_<field_name>

# 28 - Initial Values for Forms
initial_data = {
        "title": "Initial title" # not a placeholder but data in that field
    }
    form = ProductForm(request.POST or None, initial=initial_data)

# 29 - Dynamic URL Routing
Changes content based on URL.
path("<int:id>/", dynamic_lookup_view, name="dynamic_lookup_view") Passes id to a viev

# 30 - Handle DoesNotExist
obj = get_object_or_404(Product, id=id)

# 31 - Delete and Confirm

# 32 - View of a List of Database Objects
queryset = Product.objects.all()  # list of objects

# 33 - Dynamic Linking of URLs
def get_absolute_url(self):
    return f"/products/{self.id}/"

# 34 - Django URLs Reverse
def get_absolute_url(self):
    return reverse("product-detail", kwargs={"id": self.id})

<a href="{{ product.get_absolute_url }}">  # url with id from list_view to detail_view
<a href="{% url 'products:product-detail' product.id %}">

# 35 - In App URLs and Namespacing
app_name ="products" # namespace name in urls.py
def get_absolute_url(self):
    return reverse("products:product-detail", kwargs={"id": self.id})

# 36 - Class Based Views - ListView
Class based views look for a template
blog/article_list.html
<app_name>/<motel_name>_<view_name>.html

pk: primary key





{{ request.path }} == /foo/bar
{% if user.is_authenticated %}
modelname = self.model._meta.verbose_name.lower() # substracts model name
python3 manage.py runscript <script_name> # load a script form "dir_name/script_name.py"
reverse('form:success') # -> /form/success
{% if make_count > 0 %}  # counts make in django html
{% load crispy_forms_tags %}; {{ form|crispy }}



