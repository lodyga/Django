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


class BugForumCreateView(LoginRequiredMixin, CreateView):
    model = BugForum
    fields = ['title', 'text']
    template_name = "forums/bug_form.html"

    def form_valid(self, form):
        # print('form_valid called')
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(BugForumCreateView, self).form_valid(form)


class FeatureForumCreateView(LoginRequiredMixin, CreateView):
    model = FeatureForum
    fields = ['title', 'text']
    template_name = "forums/feature_form.html"

    def form_valid(self, form):
        # print('form_valid called')
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(FeatureForumCreateView, self).form_valid(form)


class BugForumUpdateView(LoginRequiredMixin, UpdateView):
    model = BugForum
    fields = ['title', 'text']
    template_name = "forums/bug_form.html"

    def get_queryset(self):
        qs = super(BugForumUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class FeatureForumUpdateView(LoginRequiredMixin, UpdateView):
    model = FeatureForum
    fields = ['title', 'text']
    template_name = "forums/feature_form.html"

    def get_queryset(self):
        qs = super(FeatureForumUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class BugForumDetailView(DetailView):
    model = BugForum
    template_name = "forums/bug_detail.html"

    def get(self, request, pk):
        forum = get_object_or_404(BugForum, pk=pk)
        comments = BugComment.objects.filter(
            forum=forum).order_by('-updated_at')
        comment_form = CommentForm()
        context = {'forum': forum,
                   'comments': comments,
                   'comment_form': comment_form}
        return render(request, self.template_name, context)


class FeatureForumDetailView(DetailView):
    model = FeatureForum
    template_name = "forums/feature_detail.html"

    def get(self, request, pk):
        forum = get_object_or_404(FeatureForum, pk=pk)
        comments = FeatureComment.objects.filter(
            forum=forum).order_by('-updated_at')
        comment_form = CommentForm()
        context = {'forum': forum,
                   'comments': comments,
                   'comment_form': comment_form}
        return render(request, self.template_name, context)


class BugCommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        f = get_object_or_404(BugForum, pk=pk)
        comment = BugComment(
            text=request.POST['comment'], owner=request.user, forum=f)
        comment.save()
        return redirect(reverse('forums:bug-forum-detail', args=[pk]))


class FeatureCommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        f = get_object_or_404(FeatureForum, pk=pk)
        comment = FeatureComment(
            text=request.POST['comment'], owner=request.user, forum=f)
        comment.save()
        return redirect(reverse('forums:feature-forum-detail', args=[pk]))

# when class CommentForm(forms.ModelForm):
# class BugCommentUpdateView(LoginRequiredMixin, View):
#     def get(self, request, pk):
#         comment = get_object_or_404(BugComment, pk=pk, owner=request.user)
#         form = CommentForm()
#         # form = CommentForm(instance=comment)
#         return render(request, 'forums/bug_comment_form.html', {'form': form})
#
#     def post(self, request, pk):
#         comment = get_object_or_404(BugComment, pk=pk, owner=request.user)
#         form = CommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('forums:bug-forum-detail', args=[comment.forum.pk]))
#         return render(request, 'forums/bug_comment_form.html', {'form': form})


# when class CommentForm(forms.Form):
class BugCommentUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        comment = get_object_or_404(BugComment, pk=pk, owner=request.user)
        form = CommentForm(initial={'comment': comment.text})
        return render(request, 'forums/bug_comment_form.html', {'form': form, 'forum': comment.forum})

    def post(self, request, pk):
        comment = get_object_or_404(BugComment, pk=pk, owner=request.user)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.text = form.cleaned_data['comment']
            comment.save()
            return redirect(reverse('forums:bug-forum-detail', args=[comment.forum.pk]))
        return render(request, 'forums/bug_comment_form.html', {'form': form, 'forum': comment.forum})


class FeatureCommentUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        comment = get_object_or_404(FeatureComment, pk=pk, owner=request.user)
        form = CommentForm(initial={'comment': comment.text})
        return render(request, 'forums/feature_comment_form.html', {'form': form, 'forum': comment.forum})

    def post(self, request, pk):
        comment = get_object_or_404(FeatureComment, pk=pk, owner=request.user)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.text = form.cleaned_data['comment']
            comment.save()
            return redirect(reverse('forums:feature-forum-detail', args=[comment.forum.pk]))
        return render(request, 'forums/feature_comment_form.html', {'form': form, 'forum': comment.forum})
