from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

app_name = 'forums'

urlpatterns = [
    # Forum index view
    path('bug_forum', views.BugForumListView.as_view(), name='bug-forum'),
    path('feature_forum', views.FeatureForumListView.as_view(), name='feature-forum'),

    # Forum detail view
    path('bug_forum/create',
         views.BugForumCreateView.as_view(success_url=reverse_lazy('forums:bug-forum')), name='bug-forum-create'),
    path('feature_forum/create',
         views.FeatureForumCreateView.as_view(success_url=reverse_lazy('forums:feature-forum')), name='feature-forum-create'),

    # Forum update view
    path('bug_forum/<int:pk>/update',
         views.BugForumUpdateView.as_view(success_url=reverse_lazy('forums:bug-forum')), name='bug-forum-update'),
    path('feature_forum/<int:pk>/update',
         views.FeatureForumUpdateView.as_view(success_url=reverse_lazy('forums:feature-forum')), name='feature-forum-update'),

    # Forum detail view
    path('bug_forum/<int:pk>', views.BugForumDetailView.as_view(),
         name='bug-forum-detail'),
    path('feature_forum/<int:pk>', views.FeatureForumDetailView.as_view(),
         name='feature-forum-detail'),

    # Comment create view
    path('bug_forum/<int:pk>/create',
         views.BugCommentCreateView.as_view(), name='bug-forum-comment-create'),
    path('feature_forum/<int:pk>/create',
         views.FeatureCommentCreateView.as_view(), name='feature-forum-comment-create'),

    # Comment update view
    path('bug_forum/<int:pk>/comment/update',
         views.BugCommentUpdateView.as_view(), name='bug-forum-comment-udpate'),
    path('feature_forum/<int:pk>/comment/update',
         views.FeatureCommentUpdateView.as_view(), name='feature-forum-comment-udpate'),


    # path('forum/<int:pk>/delete',
    #      views.ForumDeleteView.as_view(success_url=reverse_lazy('forums:all')), name='forum_delete'),
    # path('comment/<int:pk>/delete',
    #      views.CommentDeleteView.as_view(success_url=reverse_lazy('forums:all')), name='forum_comment_delete'),
]
