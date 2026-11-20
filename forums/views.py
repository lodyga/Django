from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from forums.models import BugForum, BugComment, FeatureForum, FeatureComment
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from forums.forms import CommentForm
from django.views import View


class BugForumListView(ListView):
    model = BugForum
    template_name = "forums/bug_forum_list.html"


class FeatureForumListView(ListView):
    model = FeatureForum
    template_name = "forums/feature_forum_list.html"


class ForumCreateView(LoginRequiredMixin, CreateView):
    fields = ['title', 'text']

    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super().form_valid(form)


class BugForumCreateView(ForumCreateView):
    model = BugForum
    template_name = "forums/bug_form.html"


class FeatureForumCreateView(ForumCreateView):
    model = FeatureForum
    template_name = "forums/feature_form.html"


class ForumUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['title', 'text']

    def get_queryset(self):
        qs = super(ForumUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class BugForumUpdateView(ForumUpdateView):
    model = BugForum
    template_name = "forums/bug_form.html"


class FeatureForumUpdateView(ForumUpdateView):
    model = FeatureForum
    template_name = "forums/feature_form.html"


class ForumDetailView(DetailView):
    def get(self, request, pk):
        forum = get_object_or_404(self.model_forum, pk=pk)
        comments = self.model_comment.objects.filter(
            forum=forum).order_by('-updated_at')
        comment_form = CommentForm()
        context = {'forum': forum,
                   'comments': comments,
                   'comment_form': comment_form}
        return render(request, self.template_name, context)


class BugForumDetailView(ForumDetailView):
    model_forum = BugForum
    model_comment = BugComment
    template_name = "forums/bug_detail.html"


class FeatureForumDetailView(ForumDetailView):
    model_forum = FeatureForum
    model_comment = FeatureComment
    template_name = "forums/feature_detail.html"


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        forum = get_object_or_404(self.model_forum, pk=pk)
        comment = self.model_comment(
            text=request.POST['comment'], owner=request.user, forum=forum)
        comment.save()
        return redirect(reverse(self.forum_detail_url_name, args=[pk]))


class BugCommentCreateView(CommentCreateView, View):
    model_forum = BugForum
    model_comment = BugComment
    forum_detail_url_name = 'forums:bug-forum-detail'


class FeatureCommentCreateView(LoginRequiredMixin, View):
    model_forum = FeatureForum
    model_comment = FeatureComment
    forum_detail_url_name = 'forums:feature-forum-detail'


class CommentUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        comment = get_object_or_404(
            self.model_comment, pk=pk, owner=request.user)
        form = CommentForm(initial={'comment': comment.text})
        return render(request, self.template_name, {'form': form, 'forum': comment.forum})

    def post(self, request, pk):
        comment = get_object_or_404(
            self.model_comment, pk=pk, owner=request.user)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.text = form.cleaned_data['comment']
            comment.save()
            return redirect(reverse(self.forum_comment_udpate_url_name, args=[comment.forum.pk]))
        return render(request, self.template_name, {'form': form, 'forum': comment.forum})


class BugCommentUpdateView(CommentUpdateView):
    model_comment = BugComment
    template_name = 'forums/bug_comment_form.html'
    forum_comment_udpate_url_name = 'forums:bug-forum-detail'


class FeatureCommentUpdateView(CommentUpdateView):
    model_comment = FeatureComment
    template_name = 'forums/feature_comment_form.html'
    forum_comment_udpate_url_name = 'forums:feature-forum-detail'
