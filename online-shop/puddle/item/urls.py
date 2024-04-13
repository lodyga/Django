from django.urls import path

from .views import detail_view, new_view, delete_view, edit_view, items_view

app_name = "item"

urlpatterns = [
    path("new/", new_view, name="new-view"),
    path("<int:pk>/", detail_view, name="detail-view"),
    path("<int:pk>/delete/", delete_view, name="delete-view"),
    path("<int:pk>/edit/", edit_view, name="edit-view"),
    path("", items_view, name="items-view"),
]
