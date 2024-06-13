from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

app_name = 'forums'

urlpatterns = [
    path('bug_forum', views.BugForumListView.as_view(), name='bug-forum'),
    path('feature_forum', views.FeatureForumListView.as_view(), name='feature-forum'),

    path('bug_forum/create',
         views.BugForumCreateView.as_view(success_url=reverse_lazy('forums:bug-forum')), name='bug-forum-create'),
    path('feature_forum/create',
         views.FeatureForumCreateView.as_view(success_url=reverse_lazy('forums:feature-forum')), name='feature-forum-create'),

     path('bug_forum/<int:pk>/update',
         views.BugForumUpdateView.as_view(success_url=reverse_lazy('forums:bug-forum')), name='bug-forum-update'),
     path('feature_forum/<int:pk>/update',
         views.FeatureForumUpdateView.as_view(success_url=reverse_lazy('forums:feature-forum')), name='feature-forum-update'),


    path('bug_forum/<int:pk>', views.BugForumDetailView.as_view(), name='bug-forum-detail'),
    path('feature_forum/<int:pk>', views.FeatureForumDetailView.as_view(), name='feature-forum-detail'),

    path('bug_forum/<int:pk>/comment',
         views.BugCommentCreateView.as_view(), name='bug-forum-comment-create'),
    path('feature_forum/<int:pk>/comment',
         views.FeatureCommentCreateView.as_view(), name='feature-forum-comment-create'),

     path('bug_forum/<int:pk>/comment/update',
         views.BugCommentUpdateView.as_view(), name='bug-forum-comment-udpate'),
     path('feature_forum/<int:pk>/comment/update',
         views.FeatureCommentUpdateView.as_view(), name='feature-forum-comment-udpate'),


    # path('', views.ForumListView.as_view(), name='all'),
    # path('forum/<int:pk>', views.ForumDetailView.as_view(), name='forum_detail'),
    # path('forum/create',
    #      views.ForumCreateView.as_view(success_url=reverse_lazy('forums:all')), name='forum_create'),
    # path('forum/<int:pk>/update',
    #      views.ForumUpdateView.as_view(success_url=reverse_lazy('forums:all')), name='forum_update'),
    # path('forum/<int:pk>/delete',
    #      views.ForumDeleteView.as_view(success_url=reverse_lazy('forums:all')), name='forum_delete'),
    # path('forum/<int:pk>/comment',
    #      views.CommentCreateView.as_view(), name='forum_comment_create'),
    # path('comment/<int:pk>/delete',
    #      views.CommentDeleteView.as_view(success_url=reverse_lazy('forums:all')), name='forum_comment_delete'),
]
