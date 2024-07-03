from django.urls import path, include
from . import views

# REST API
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, DifficultyViewSet, ComplexityViewSet, LanguageViewSet, ProblemViewSet, SolutionViewSet

app_name = "python_problems"

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'difficulties', DifficultyViewSet)
router.register(r'complexities', ComplexityViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'problems', ProblemViewSet)
router.register(r'solutions', SolutionViewSet)


urlpatterns = [
    # REST API
    path("api/", include(router.urls), name="api"),

    path("tag/", views.TagIndexView.as_view(), name="tag-index"),
    path("tag/create/", views.TagCreate.as_view(), name="tag-create"),

    # Tag update/delete
    # path("tag/<int:pk>/update/", views.TagUpdate.as_view(), name="tag-update"),
    # path("tag/<int:pk>/delete/", views.TagDelete.as_view(), name="tag-delete"),

    path("tag/graph/", views.tag_graph_view, name="tag-graph"),

    path("", views.ProblemIndexView.as_view(), name="problem-index"),
    path("problem_create/", views.ProblemCreate.as_view(),
         name="problem-create"),  # create have to be befre slug
    path("solution_create/", views.SolutionCreate.as_view(),
         name="solution-create"),  # create have to be befre slug
    path("language_add/", views.LanguageCreate.as_view(), name="language-create"),

    # path("<int:pk>/<str:language>/", views.ProblemDetailPkView.as_view(), name="problem-detail"),
    path("<slug:slug>/<str:language>/",
         views.ProblemDetailView.as_view(), name="problem-detail"),
    path("problem/<int:pk>/update/",
         views.ProblemUpdate.as_view(), name="problem-update"),
    path("problem/<int:pk>/delete/",
         views.ProblemDelete.as_view(), name="problem-delete"),

    path("solution/<int:pk>/update/",
         views.SolutionUpdate.as_view(), name="solution-update"),
    path("solution/<int:pk>/delete/",
         views.SolutionDelete.as_view(), name="solution-delete"),

]
