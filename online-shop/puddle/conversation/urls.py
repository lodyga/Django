from django.urls import path

from . import views

app_name = "conversation"

urlpatterns = [
    path("", views.inbox_view, name="inbox-view"),
    path("<int:pk>/", views.detail_view, name="detail-view"),
    path("new/<int:item_pk>/", views.new_view, name="new-view")
]
