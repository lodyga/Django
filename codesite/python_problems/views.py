from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Tag, Problem


class IndexView(generic.ListView):
    model = Problem


class DetailView(generic.DetailView):
    model = Problem

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        problem = self.get_object()
        context["tags"] = problem.tags.values_list("name", flat=True)
        return context

class TagIndexView(generic.ListView):
    model = Tag


class TagCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy('python_problems:tag-index')


class ProblemCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Problem
    fields = "__all__"
    success_url = reverse_lazy('python_problems:index')
