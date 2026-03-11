from django.urls import path
from . import views


app_name = "animations"

urlpatterns = [
    # path("", views.TestListView.as_view(), name="amination-index")
    path("grid_dfs", views.GridDfs.as_view(), name="grid-dfs"),
    path("grid_bfs", views.GridBfs.as_view(), name="grid-bfs"),
    path("queue", views.Queue.as_view(), name="animate-queue"),
    path("stack", views.Stack.as_view(), name="animate-stack"),
    path("deque", views.Deque.as_view(), name="animate-deque"),
    path("linked_list", views.LinkedList.as_view(), name="animate-linked-list"),
]
