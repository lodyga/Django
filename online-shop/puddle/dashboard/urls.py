from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index_view, name="index-view"),
    path("<int:pk>/category/", views.category_view, name="category-view")
]
