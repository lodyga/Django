from django.urls import path

from . import views

app_name = "python_problems"

urlpatterns = [
    path("tag/", views.TagIndexView.as_view(), name="tag-index"),
    path("tag/create/", views.TagCreate.as_view(), name="tag-create"),
    path("tag/<int:pk>/update/", views.TagUpdate.as_view(), name="tag-update"),
    path("tag/<int:pk>/delete/", views.TagDelete.as_view(), name="tag-delete"),

    path("", views.ProblemIndexView.as_view(), name="index"),
    # path("", views.problem_index_view, name="index"),
    path("<int:pk>/", views.ProblemDetailView.as_view(), name="detail"),
    # path("<int:pk>/", views.problem_detail_view, name="detail"),
    path("create/", views.ProblemCreate.as_view(), name="problem-create"),
    path("problem/<int:pk>/update/", views.ProblemUpdate.as_view(), name="problem-update"),
    path("problem/<int:pk>/delete/", views.ProblemDelete.as_view(), name="problem-delete"),
    
    path("conversion/", views.conversion_view, name="conversion"),
]