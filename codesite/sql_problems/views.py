from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.conf import settings

from .models import Tag, Problem
from . import utils
from . import urls

import pandas as pd


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
    mtcars_pd = pd.read_csv(settings.BASE_DIR / urls.app_name /
                             'static' / urls.app_name / "mtcars.csv").head(4)
    file_path = settings.BASE_DIR / urls.app_name / \
        'static' / urls.app_name / 'convert_pd.py'
    with open(file_path, 'r') as file:
        code_content = file.read()


    context = {
        "mtcars_pd": mtcars_pd,
        "mtcars_pd_dict": mtcars_pd.to_dict(),
        "mtcars_pd_dict_list": mtcars_pd.to_dict("list"),
        "mtcars_pd_dict_rec": mtcars_pd.to_dict("records"),
        "code_content": code_content,
    }
    return render(request, "sql_problems/conversion.html", context)


def ascii_view(request):

    ascii_object_table = """
| personId | lastName | firstName |
| -------- | -------- | --------- |
| 1        | Wang     | Allen     |
| 2        | Alice    | Bob       |
"""

    ascii_type_table = """
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| personId    | int     |
| lastName    | varchar |
| firstName   | varchar |
+-------------+---------+
"""

    object_table = utils.ascii_table_to_dict(ascii_object_table)
    type_table = utils.ascii_type_to_dict(ascii_type_table)
    object_df = pd.DataFrame(object_table)
    object_df = utils.change_dtype(object_df, type_table)

    # file_path = os.path.join(settings.BASE_DIR, urls.app_name, 'static', urls.app_name, 'create_db.py')
    file_path = settings.BASE_DIR / urls.app_name / \
        'static' / urls.app_name / 'create_db.py'
    with open(file_path, 'r') as file:
        code_content = file.read()

    context = {
        "ascii_object_table": ascii_object_table,
        "ascii_type_table": ascii_type_table,
        "object_df": object_df.to_dict,
        "object_df_dtypes": object_df.dtypes,
        "code_content": code_content,
    }

    return render(request, "sql_problems/ascii.html", context)
