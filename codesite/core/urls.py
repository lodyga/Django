from django.urls import path, include
from django.contrib.auth import views

from . import views

app_name = "core"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("contact/", views.contact_view, name="contact"),
    path("chat/cohere/stream/", views.cohere_stream_view, name="cohere-stream"),
    path("chat/gemini/stream/", views.gemini_stream_view, name="gemini-stream"),
    path("chat/mistral/stream/", views.mistral_stream_view, name="mistral-stream"),
    path("chat/cerberas/stream/", views.cerberas_stream_view, name="cerberas-stream"),
]
