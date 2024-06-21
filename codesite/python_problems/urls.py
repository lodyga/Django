from django.urls import path

from . import views

app_name = "python_problems"

urlpatterns = [
    path("tag/", views.TagIndexView.as_view(), name="tag-index"),
    path("tag/create/", views.TagCreate.as_view(), name="tag-create"),
    
    # Tag update/delete
    # path("tag/<int:pk>/update/", views.TagUpdate.as_view(), name="tag-update"),
    # path("tag/<int:pk>/delete/", views.TagDelete.as_view(), name="tag-delete"),

    path("tag/graph/", views.tag_graph_view, name="tag-graph"),

    path("", views.ProblemIndexView.as_view(), name="problem-index"),
    path("problem_create/", views.ProblemCreate.as_view(), name="problem-create"), # create have to be befre slug
    path("solution_create/", views.SolutionCreate.as_view(), name="solution-create"), # create have to be befre slug

    path("<slug:slug>/<str:language>/", views.ProblemDetailView.as_view(), name="problem-detail"),
    path("problem/<int:pk>/update/", views.ProblemUpdate.as_view(), name="problem-update"),
    path("problem/<int:pk>/delete/", views.ProblemDelete.as_view(), name="problem-delete"),
    
    path("solution/<int:pk>/update/", views.SolutionUpdate.as_view(), name="solution-update"),
    path("solution/<int:pk>/delete/", views.SolutionDelete.as_view(), name="solution-delete"),

]