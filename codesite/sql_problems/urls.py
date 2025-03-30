from django.urls import path

from . import views

app_name = "sql_problems"

urlpatterns = [
    # path("", views.ProblemIndexView.as_view(), name="index"),
    path("conversion/", views.conversion_view, name="conversion"),
    path("ascii/", views.ascii_view, name="ascii"),
]
