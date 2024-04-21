from django.urls import path

from . import views

app_name = "python_problems"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("tag/", views.TagIndexView.as_view(), name="tag_index"),
    path("tag/create/", views.TagCreate.as_view(), name="tag-create"),
    path("create/", views.ProblemCreate.as_view(), name="problem_create"),
]