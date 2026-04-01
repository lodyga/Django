from django.urls import path, include
from django.contrib.auth import views

from . import views

app_name = "core"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("contact/", views.contact_view, name="contact"),
    path("chat/stream/", views.cohere_stream_view, name="cohere-stream"),
]
