from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from rest_framework import viewsets
from .forms import (
    ProblemForm,
    SolutionCreateForm,
    SolutionUpdateForm,
    ProblemTestCaseCreateForm,
    ProblemTestCaseUpdateForm,
)
from .models import (
    Problem,
    Tag,
    Solution,
    Language,
    ProblemTestCase,
    Difficulty,
    Complexity,
)
from .serializers import (
    TagSerializer,
    DifficultySerializer,
    ComplexitySerializer,
    LanguageSerializer,
    ProblemSerializer,
    SolutionSerializer,
)
from .services.ui_problem_test_cases import (
    get_ui_problem_test_cases,
    get_effective_problem_test_cases,
    get_clipboard_problem_test_cases
)
from .services.code_assembly import (
    get_problem_type_header,
    get_placeholder_source_code
)
from .services.judge0 import execute_code
from .services.problem_helpers import (
    parse_url,
    get_adjacent_slugs,
    parse_problem_description
)


def tag_graph_view(request):
    tag_list = (Tag.objects
                .annotate(problem_count=Count("problem"))
                .order_by("-problem_count"))

    data = [
        {"tag": tag.name, "count": tag.problem_count}
        for tag in tag_list
    ]
    return render(request, "python_problems/tag_graph.html", {"data": data})


class NextUrlMixin():
    request: HttpRequest

    def _get_next_url(self):
        next_url = (
            self.request.POST.get("next")
            or self.request.GET.get("next")
        )
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return next_url
        return None

    def get_fallback_next_url(self):
        return None

    def get_redirect_url(self):
        return (
            self._get_next_url()
            or self.get_fallback_next_url()
            or reverse_lazy("python_problems:problem-index")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next_url"] = self.get_redirect_url()
        return context

    def get_success_url(self):
        return self.get_redirect_url()


class ProblemIndexView(ListView):
    model = Problem
    template_name = "python_problems/problem_list.html"

    def get_queryset(self):
        queryset = (
            Problem.objects
            .select_related("difficulty", "owner")
            .prefetch_related("tags", "solutions__language")
        )

        query_text = self.request.GET.get("query_text")
        difficulty_id = self.request.GET.get("difficulty_id")
        tag_id = self.request.GET.get("tag_id")
        language_id = self.request.GET.get("language_id")
        order_by = self.request.GET.get("order_by", "created_at")

        if difficulty_id and difficulty_id != "0":
            queryset = queryset.filter(difficulty_id=difficulty_id)

        if language_id and language_id != "0":
            queryset = queryset.filter(solutions__language_id=language_id)

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

        for problem in page_problems:
            problem.languages = {
                solution.language
                for solution in problem.solutions.all()
            }

        context["difficulty_list"] = Difficulty.objects.all()
        context["problem_list"] = Problem.objects.all()
        context["tag_list"] = Tag.objects.all()
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


class ProblemDetailView(NextUrlMixin, DetailView):
    model = Problem
    template_name = "python_problems/problem_detail.html"  # needed for post render()

    def _get_owner_solution_context(self, problem, owner, language):
        owner_solutions = Solution.objects.filter(
            problem=problem,
            language=language,
            owner=owner
        )
        owner_all_solutions = Solution.objects.filter(
            problem=problem,
            owner=owner
        )
        owner_solution_languages = Language.objects.filter(
            id__in=owner_all_solutions.values_list("language", flat=True)
        )
        solution_languages = Language.objects.filter(
            id__in=owner_all_solutions.values_list("language", flat=True)
        )
        for solution in owner_solutions:
            solution.source_code = get_problem_type_header(
                problem.problem_type,
                language
            ) + solution.source_code

        return {
            "solution_languages": solution_languages,
            "owner_solutions": owner_solutions,
            "owner_all_solutions": owner_all_solutions,
            "owner_solution_languages": owner_solution_languages,
        }

    def get_context_data(self, **kwargs):
        # fetch get_context_data() from DetailView
        context = super().get_context_data(**kwargs)
        User = get_user_model()

        # get current problem
        problem = self.get_object()

        # Get current language from URL
        language = Language.objects.get(name=self.kwargs.get("language"))

        language_solutions = Solution.objects.filter(
            problem=problem,
            language=language
        )
        # Get the list of the owners who have solutions for the problem and language;
        owners = User.objects.filter(
            id__in=language_solutions.values_list("owner", flat=True)
        )
        # Prefer the current user's solutions when available.
        preferred_owner = None
        if self.request.user.is_authenticated:
            preferred_owner = owners.filter(id=self.request.user.id).first()
        owner = preferred_owner or owners.first()
        solution_owner_id = owner.id

        owner_solution_data = self._get_owner_solution_context(
            problem=problem,
            owner=owner,
            language=language,
        )
        owner_solutions = owner_solution_data["owner_solutions"]
        solution_languages = owner_solution_data["solution_languages"]
        owner_solution_languages = owner_solution_data["owner_solution_languages"]
        # Multiple solutions are allowed; use the first ordered solution.
        selected_solution = owner_solutions.first()

        ui_problem_test_cases = get_ui_problem_test_cases(
            problem, selected_solution, language.name
        )
        effective_problem_test_cases = get_effective_problem_test_cases(
            problem,
            selected_solution,
            language,
        )
        clipboard_problem_test_cases = get_clipboard_problem_test_cases(
            problem,
            selected_solution,
            language,
        )
        url = parse_url(problem.url)
        source_code = get_placeholder_source_code(language)
        tag_list = problem.tags.all()

        # Get related problems.
        common_tags = Count("tags", filter=Q(tags__in=problem.tags.all()))
        related_problems = (
            Problem.objects
            .annotate(common_tags=common_tags)
            .filter(common_tags__gte=3)
            .exclude(pk=problem.pk)
            .distinct())

        prev_problem_slug, next_problem_slug = get_adjacent_slugs(problem)

        (question, examples) = parse_problem_description(problem.description)

        context.update({
            "clipboard_problem_test_cases": clipboard_problem_test_cases,
            "effective_problem_test_cases": effective_problem_test_cases,
            "examples": examples,
            "language": language,
            "language_id": language.id,
            'next_problem_slug': next_problem_slug,
            "output_container": "null",
            "owner_id": solution_owner_id,
            "solution_owner_id": solution_owner_id,
            "owner_solution_languages": owner_solution_languages,
            "owner_solutions": owner_solutions,
            "owners": owners,
            'prev_problem_slug': prev_problem_slug,
            "problem_slug": problem.slug,
            "question": question,
            "related_problems": related_problems,
            "solution": selected_solution,
            "solution_languages": solution_languages,
            "source_code": source_code,
            "tag_list": tag_list,
            "ui_problem_test_cases": ui_problem_test_cases,
            "url": url,
        })
        return context

    def post(self, request, **kwargs):
        problem = self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        User = get_user_model()

        button_pressed = request.POST.get("code_form_action")
        is_code_container_filled = "code_container" in request.POST

        if "language_id" in request.POST:
            language_id = request.POST.get("language_id")
            language = get_object_or_404(Language, id=language_id)
            return redirect("python_problems:problem-detail", problem.slug, language.name)

        language_id = context["language_id"]
        language = get_object_or_404(Language, id=language_id)

        solution_owner_id = int(
            request.POST.get("solution_owner_id")
            or request.POST.get("owner_id")
            or context["solution_owner_id"]
        )
        owner = get_object_or_404(User, id=solution_owner_id)

        owner_solution_data = self._get_owner_solution_context(
            problem=problem,
            owner=owner,
            language=language,
        )
        owner_solutions = owner_solution_data["owner_solutions"]
        owner_solution_languages = owner_solution_data["owner_solution_languages"]
        solution_languages = owner_solution_data["solution_languages"]

        # Run or validate code
        if (
            button_pressed and
            is_code_container_filled
        ):
            source_code = request.POST.get("code_container")
            output = execute_code(
                problem,
                source_code,
                language.name,
                button_pressed,
                context["effective_problem_test_cases"]
            )
            output_container = output
        else:
            source_code = context["source_code"]
            output_container = context["output_container"]

        context.update({
            "source_code": source_code,
            "language": language,
            "language_id": language_id,
            "output_container": output_container,
            "owner_id": solution_owner_id,
            "solution_owner_id": solution_owner_id,
            "owner_solution_languages": owner_solution_languages,
            "owner_solutions": owner_solutions,
            "solution_languages": solution_languages,
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


class ProblemCreate(LoginRequiredMixin, NextUrlMixin, CreateView):
    model = Problem
    form_class = ProblemForm
    success_url = reverse_lazy('python_problems:problem-index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProblemUpdate(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = Problem
    form_class = ProblemForm
    success_url = reverse_lazy('python_problems:problem-index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ProblemDelete(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = Problem
    fields = "__all__"
    success_url = reverse_lazy('python_problems:problem-index')


class SolutionCreate(LoginRequiredMixin, NextUrlMixin, CreateView):
    model = Solution
    form_class = SolutionCreateForm
    success_url = reverse_lazy('python_problems:problem-index')

    def get_initial(self):
        initial = super().get_initial()
        for field_name in ("problem", "language", "order"):
            if value := self.request.GET.get(field_name):
                initial[field_name] = value
        return initial

    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super().form_valid(form)


class SolutionUpdate(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = Solution
    # Custom form to exclude = ["problem", "language", "owner"] fields.
    form_class = SolutionUpdateForm
    success_url = reverse_lazy('python_problems:problem-index')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_initial(self):
        initial = super().get_initial()
        for field_name in ("problem", "language", "order"):
            if value := self.request.GET.get(field_name):
                initial[field_name] = value
        return initial

    def get_fallback_next_url(self):
        return reverse_lazy(
            "python_problems:problem-detail",
            kwargs={
                "slug": self.object.problem.slug,
                "language": self.object.language.name,
            },
        )

    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super().form_valid(form)


class SolutionDelete(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = Solution
    fields = "__all__"
    success_url = reverse_lazy('python_problems:problem-index')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_fallback_next_url(self):
        return reverse_lazy(
            "python_problems:problem-detail",
            kwargs={
                "slug": self.object.problem.slug,
                "language": self.object.language.name,
            },
        )


class LanguageCreate(LoginRequiredMixin, NextUrlMixin, CreateView):
    model = Language
    fields = ["name"]
    success_url = reverse_lazy('python_problems:problem-index')


class ProblemTestCaseCreate(LoginRequiredMixin, NextUrlMixin, CreateView):
    model = ProblemTestCase
    form_class = ProblemTestCaseCreateForm
    success_url = reverse_lazy('python_problems:problem-index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProblemTestCaseUpdate(LoginRequiredMixin, NextUrlMixin, UpdateView):
    model = ProblemTestCase
    form_class = ProblemTestCaseUpdateForm
    success_url = reverse_lazy('python_problems:problem-index')

    def get_queryset(self):
        return ProblemTestCase.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProblemTestCaseDelete(LoginRequiredMixin, NextUrlMixin, DeleteView):
    model = ProblemTestCase
    success_url = reverse_lazy('python_problems:problem-index')

    def get_queryset(self):
        return ProblemTestCase.objects.filter(owner=self.request.user)


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
