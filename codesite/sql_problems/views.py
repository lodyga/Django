from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Tag, Problem

class ProblemIndexView(ListView):
    model = Problem

    def get_context_data(self, **kwargs):
        context = super(ProblemIndexView, self).get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        problem_list = self.model.objects.all()

        if query:
            problem_list = problem_list.filter(
                Q(tags__name__icontains=query) | Q(title__icontains=query)).distinct()

        context["problem_list"] = problem_list
        context["query"] = query
        return context

class ProblemDetailView(DetailView):
    model = Problem

    def get_context_data(self, **kwargs):
        context = super(ProblemDetailView, self).get_context_data(**kwargs)
        problem = self.get_object()
        context["tags"] = problem.tags.values_list("name", flat=True)
        context["related_problems"] = Problem.objects.filter(
            tags__in=problem.tags.all()).exclude(pk=problem.pk).distinct()
        return context

class ProblemCreate(LoginRequiredMixin, CreateView):
    model = Problem
    fields = "__all__"
    success_url = reverse_lazy('python_problems:index')


class ProblemUpdate(LoginRequiredMixin, UpdateView):
    model = Problem
    fields = "__all__"
    success_url = reverse_lazy('python_problems:index')


class ProblemDelete(LoginRequiredMixin, DeleteView):
    model = Problem
    fields = "__all__"
    success_url = reverse_lazy('python_problems:index')

def conversion_view(request):
    return render(request, "sql_problems/conversion.html")
