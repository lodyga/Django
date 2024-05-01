from django.urls import path

from . import views

app_name = "sql_problems"

urlpatterns = [
    path("", views.ProblemIndexView.as_view(), name="index"),
    # path("", views.problem_index_view, name="index"),
    path("<int:pk>/", views.ProblemDetailView.as_view(), name="detail"),
    # path("<int:pk>/", views.problem_detail_view, name="detail"),
    path("create/", views.ProblemCreate.as_view(), name="problem-create"),
    path("problem/<int:pk>/update/", views.ProblemUpdate.as_view(), name="problem-update"),
    path("problem/<int:pk>/delete/", views.ProblemDelete.as_view(), name="problem-delete"),

    path("conversion/", views.conversion_view, name="conversion"),
    path("ascii/", views.ascii_view, name="ascii"),
]
