# from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from rest_framework import viewsets
from .forms import *
from .models import *
from .serializers import *
from .scripts import *
from core.scripts import *


def tag_graph_view(request):
    tag_list = (Tag.objects
                .annotate(problem_count=Count("problem"))
                .order_by("-problem_count"))

    data = [
        {"tag": tag.name, "count": tag.problem_count}
        for tag in tag_list
    ]
    return render(request, "python_problems/tag_graph.html", {"data": data})


class ProblemIndexView(ListView):
    model = Problem
    template_name = "python_problems/problem_list.html"

    def get_queryset(self):
        queryset = (
            Problem.objects
            .select_related("difficulty", "owner")
            .prefetch_related("tags", "solution_set__language")
        )

        query_text = self.request.GET.get("query_text")
        difficulty_id = self.request.GET.get("difficulty_id")
        tag_id = self.request.GET.get("tag_id")
        language_id = self.request.GET.get("language_id")
        order_by = self.request.GET.get("order_by", "created_at")

        if difficulty_id and difficulty_id != "0":
            queryset = queryset.filter(difficulty_id=difficulty_id)

        if language_id and language_id != "0":
            queryset = queryset.filter(solution__language_id=language_id)

        if tag_id and tag_id != "0":
            queryset = queryset.filter(tags__id=tag_id)

        if query_text:
            queryset = queryset.filter(
                Q(tags__name__icontains=query_text) |
                Q(title__icontains=query_text)
            ).distinct()

        return queryset.order_by(order_by)

    def get_paginate_by(self, queryset):
        return int(self.request.GET.get("problems_per_page", 7))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_problems = list(context["page_obj"].object_list)
        problem_ids = [problem.id for problem in page_problems]

        solution_language_rows = (
            Solution.objects
            .filter(problem_id__in=problem_ids)
            .values("problem_id", "language__name")
            .distinct()
            # .order_by("problem_id", "language__name")
        )
        problem_languages = {}
        for row in solution_language_rows:
            problem_id = row["problem_id"]
            language_name = row["language__name"]
            problem_languages.setdefault(problem_id, []).append(language_name)

        context["difficulty_list"] = Difficulty.objects.all()
        context["problem_list"] = Problem.objects.all()
        context["tag_list"] = Tag.objects.all()
        context["problem_languages"] = problem_languages
        context["language_list"] = (
            Language.objects
            .annotate(solution_count=Count("solution"))
            .order_by("-solution_count")
        )
        context["difficulty_id"] = int(
            self.request.GET.get("difficulty_id", 0))
        context["language_id"] = int(self.request.GET.get("language_id", 0))
        context["tag_id"] = int(self.request.GET.get("tag_id", 0))
        context["query_text"] = self.request.GET.get("query_text", "")
        context["order_by"] = self.request.GET.get("order_by", "created_at")
        context["problems_per_page"] = self.get_paginate_by(
            self.get_queryset()
        )
        context["problems_per_page_options"] = [
            5, 6, 7, 8, 10, 15, 20, 50, 100, len(Problem.objects.all())]

        params = self.request.GET.copy()
        params.pop("page", None)
        # keep all active filters/sort/per-page values.
        context["querystring"] = params.urlencode()

        return context


class ProblemDetailView(DetailView):
    model = Problem
    template_name = "python_problems/problem_detail.html"  # needed for post render()

    def get_context_data(self, **kwargs):
        # fetch get_context_data() from DetailView
        context = super().get_context_data(**kwargs)
        User = get_user_model()

        # get current problem
        problem = self.get_object()

        # Get current language from URL
        language_name = self.kwargs.get("language")
        language = Language.objects.get(name=language_name)
        del language_name
        language_id = language.id

        solutions = Solution.objects.filter(
            problem=problem,
            language=language)

        # Get the list of the owners who have solutions for the problem and language;
        owners = User.objects.filter(
            id__in=solutions.values_list("owner", flat=True))

        # Get current owner id from the owner form-select
        # (if none selected take the first owner from owners)
        owner_id = owners.first().id

        # Get owner from owner id.
        owner = User.objects.get(id=owner_id)

        # Get all languages for owners problem.
        language_ids = (
            Solution.objects
            .filter(problem=problem, owner=owner)
            .values_list("language", flat=True))
        solution_languages = Language.objects.filter(id__in=language_ids)

        solutions = Solution.objects.filter(
            problem=problem,
            language=language,
            owner=owner)

        # There's only one solution per owner and language
        solution = solutions.first()

        test_cases = clean_test_cases(solution.test_cases)
        url = parse_url(problem.url)
        source_code = get_placeholder_source_code(language.id)
        tag_list = problem.tags.all()

        # Get related problems.
        common_tags = Count("tags", filter=Q(tags__in=problem.tags.all()))
        related_problems = (
            Problem.objects
            .annotate(common_tags=common_tags)
            .filter(common_tags__gte=3)
            .exclude(pk=problem.pk)
            .distinct())

        # Get adjacent problem slugs
        prev_problem_slug, next_problem_slug = get_adjacent_slugs(
            problem, language)

        (question, examples) = parse_problem_description(problem.description)

        context.update({
            "examples": examples,
            "language": language,
            "language_id": language_id,
            'next_problem_slug': next_problem_slug,
            "output_container": "null",
            "owner_id": owner_id,
            "owners": owners,
            'prev_problem_slug': prev_problem_slug,
            "question": question,
            "raw_test_cases": solution.test_cases,
            "related_problems": related_problems,
            "solution": solution,
            "solution_languages": solution_languages,
            "source_code": source_code,
            "tag_list": tag_list,
            "test_cases": test_cases,
            "url": url,
        })
        return context

    def post(self, request, **kwargs):
        problem = self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        User = get_user_model()

        is_run_code_button_pressed = request.POST.get(
            "code_form_action") == "run"
        is_test_code_button_pressed = request.POST.get(
            "code_form_action") == "test"
        # is_submit_code_button_pressed = request.POST.get("code_form_action") == "submit"
        is_code_container_filled = "code_container" in request.POST

        # if "message" in request.POST:
        #     return get_cohere_response(request)

        if "language_id" in request.POST:
            language_id = request.POST.get("language_id")
            language = get_object_or_404(Language, id=language_id)
            return redirect("python_problems:problem-detail", problem.slug, language.name)

        language_id = context["language_id"]
        language = get_object_or_404(Language, id=language_id)

        owner_id = int(request.POST.get("owner_id", context["owner_id"]))
        owner = get_object_or_404(User, id=owner_id)

        solution = Solution.objects.filter(
            problem=problem,
            owner=owner,
            language=language).first()

        # Run code
        if (
            is_run_code_button_pressed and
            is_code_container_filled
        ):
            source_code = request.POST.get("code_container")
            output = execute_code(source_code, language.name)
            output_container = output
        # Validate code
        elif (
            is_test_code_button_pressed and
            is_code_container_filled
        ):
            source_code = request.POST.get("code_container")
            test_cases = context["test_cases"]
            output = validate_code(source_code, language.name, test_cases)
            output_container = output
        else:
            source_code = context["source_code"]
            output_container = context["output_container"]

        context.update({
            "source_code": source_code,
            "language_id": language_id,
            "output_container": output_container,
            "owner_id": owner_id,
            "raw_test_cases": solution.test_cases,
            "solution": solution,
        })
        return render(request, self.template_name, context)


class TagIndexView(ListView):
    model = Tag


class TagCreate(LoginRequiredMixin, CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy('python_problems:tag-index')


class TagUpdate(LoginRequiredMixin, UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy('python_problems:tag-index')


class TagDelete(LoginRequiredMixin, DeleteView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy('python_problems:tag-index')


class ProblemCreate(LoginRequiredMixin, CreateView):
    model = Problem
    form_class = ProblemForm  # Custom form to remove "slug", "owner" fields
    success_url = reverse_lazy('python_problems:problem-index')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super().form_valid(form)


class ProblemUpdate(LoginRequiredMixin, UpdateView):
    model = Problem
    form_class = ProblemForm
    success_url = reverse_lazy('python_problems:problem-index')


class ProblemDelete(LoginRequiredMixin, DeleteView):
    model = Problem
    fields = "__all__"
    success_url = reverse_lazy('python_problems:problem-index')


class SolutionCreate(LoginRequiredMixin, CreateView):
    model = Solution
    form_class = SolutionCreateForm  # Custom form to remove "owner" field.
    success_url = reverse_lazy('python_problems:problem-index')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super().form_valid(form)


class SolutionUpdate(LoginRequiredMixin, UpdateView):
    model = Solution
    # Custom form to exclude = ["problem", "language", "owner"] fields.
    form_class = SolutionUpdateForm
    success_url = reverse_lazy('python_problems:problem-index')


class SolutionDelete(LoginRequiredMixin, DeleteView):
    model = Solution
    fields = "__all__"
    success_url = reverse_lazy('python_problems:problem-index')


class LanguageCreate(LoginRequiredMixin, CreateView):
    model = Language
    fields = ["name"]
    success_url = reverse_lazy('python_problems:problem-index')


# REST API
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class DifficultyViewSet(viewsets.ModelViewSet):
    queryset = Difficulty.objects.all()
    serializer_class = DifficultySerializer


class ComplexityViewSet(viewsets.ModelViewSet):
    queryset = Complexity.objects.all()
    serializer_class = ComplexitySerializer


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class SolutionViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
