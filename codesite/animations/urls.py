from django.urls import path
from . import views


app_name = "animations"

urlpatterns = [
    # path("", views.TestListView.as_view(), name="amination-index")
    path("grid_dfs", views.GridDfs.as_view(), name="grid-dfs"),
    path("grid_bfs", views.GridBfs.as_view(), name="grid-bfs"),
    path("grid_bfs", views.Queue.as_view(), name="grid-bfs"),

]