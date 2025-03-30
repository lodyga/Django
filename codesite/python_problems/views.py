# from django.conf import settings
import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .cohere_auth import COHERE_API_KEY
from .forms import OutputForm, ProblemForm, SolutionForm
from .models import Complexity, Difficulty, Language, Problem, Solution, Tag
from .static.python_problems.scripts import *

# REST API
from rest_framework import viewsets
from .serializers import (
    ComplexitySerializer,
    DifficultySerializer,
    LanguageSerializer,
    ProblemSerializer,
    SolutionSerializer,
    TagSerializer
)


def tag_graph_view(request):
    tag_list = Tag.objects.all()
    data = [{"tag": tag.name,
             "count": tag.problem_set.count()}
            for tag in tag_list]
    sorted_data = sorted(data, key=lambda x: x["count"], reverse=True)
    return render(request, "python_problems/tag_graph.html", {"data": sorted_data})


class ProblemIndexView(ListView):
    model = Problem  # Problem model
    template_name = "python_problems/problem_list.html"  # needed for post render()

    def get_context_data(self, **kwargs):
        # fetch get_context_data from parent class
        context = super().get_context_data(**kwargs)

        # Get data from database.
        difficulty_list = Difficulty.objects.all()
        problem_list = Problem.objects.all()
        tag_list = Tag.objects.all()
        language_list = Language.objects.all()

        # Problems pagination.
        problems_per_page = 7
        paginator = Paginator(problem_list, problems_per_page)
        page_obj = paginator.get_page(1)

        # Get solution languages for each problem
        problems_languages = {}
        for problem in problem_list[:problems_per_page]:
            language_indexes = (
                Solution.objects
                .filter(problem=problem)
                .values_list("language", flat=True))
            problem_languages_list = Language.objects.filter(
                id__in=language_indexes)
            del language_indexes
            problems_languages[problem] = problem_languages_list

        # Option values for problems_per_page form-select.
        problems_per_page_options = [
            5, 6, 7, 8, 10, 15, 20, 50, 100, len(problem_list)
        ]

        context.update({
            "difficulty_id": 0,
            "difficulty_list": difficulty_list,
            "language_id": 0,
            "language_list": language_list,
            "order_by": "created_at",
            "page_obj": page_obj,
            "problems_languages": problems_languages,
            "problem_list": problem_list,
            "problems_per_page": problems_per_page,
            "problems_per_page_options": problems_per_page_options,
            "tag_id": 0,
            "tag_list": tag_list,
            "query_text": "",
        })
        return context

    def post(self, request, **kwargs):
        # Explicitly fetch object_list (since ListView doesn't do it in POST)
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        problem_list = Problem.objects.all()

        # Get data from request POST.
        query_text = request.POST.get("query_text", context["query_text"])
        difficulty_id = int(request.POST.get(
            "difficulty_id", context["difficulty_id"]))
        tag_id = int(request.POST.get("tag_id", context["tag_id"]))
        language_id = int(request.POST.get(
            "language_id", context["language_id"]))
        order_by = request.POST.get("order_by", context["order_by"])
        problems_per_page = int(request.POST.get(
            "problems_per_page", context["problems_per_page"]))
        # problems_per_page = int(request.POST.get("problems_per_page") or context["problems_per_page"])
        page_number = int(request.POST.get("page_number")
                          or request.POST.get("form_page_number", 1))

        # Fileter problems by difficulty.
        if difficulty_id:
            difficulty = get_object_or_404(Difficulty, id=difficulty_id)
            problem_list = problem_list.filter(difficulty=difficulty)

        # Fileter problems by language.
        if language_id:
            language = get_object_or_404(Language, id=language_id)
            problem_list = problem_list.filter(solution__language=language)

        # Fileter problems by tag.
        if tag_id:
            tag = get_object_or_404(Tag, id=tag_id)
            problem_list = problem_list.filter(tags=tag)

        # Filter problems by query text from search form.
        if query_text:
            problem_list = (
                problem_list
                .filter(Q(tags__name__icontains=query_text) | Q(title__icontains=query_text))
                .distinct())

        # Order problems.
        problem_list = problem_list.order_by(order_by)

        # Paginate problems.
        paginator = Paginator(problem_list, problems_per_page)
        page_obj = paginator.get_page(page_number)

        # Get solution languages for problems on `page_number` page.
        start = (page_number - 1) * problems_per_page
        end = start + problems_per_page
        problems_languages = {}
        for problem in problem_list[start:end]:
            language_indexes = (
                Solution.objects
                .filter(problem=problem)
                .values_list("language", flat=True))
            language_list = Language.objects.filter(id__in=language_indexes)
            del language_indexes
            problems_languages[problem] = language_list

        context.update({
            "difficulty_id": difficulty_id,
            "language_id": language_id,
            "order_by": order_by,
            "page_number": page_number,
            "page_obj": page_obj,
            "problems_languages": problems_languages,
            "problem_list": problem_list,
            "problems_per_page": problems_per_page,
            "query_text": query_text,
            "tag_id": tag_id,
        })
        return render(request, self.template_name, context)


class ProblemDetailView(DetailView):
    model = Problem  # Problem model
    template_name = "python_problems/problem_detail.html"  # needed for post render()

    def get_context_data(self, **kwargs):
        # fetch get_context_data() from DetailView
        context = super().get_context_data(**kwargs)

        User = get_user_model()

        # get current problem
        problem = self.get_object()

        # Get current language from the URL
        language_name = self.kwargs.get("language")

        # get the language model  # Language.objects.get(name="Python")
        language = get_object_or_404(Language, name=language_name)
        del language_name

        # solution language id
        language_id = language.id

        # Get solutions for all users based on the problem and the language
        solutions = Solution.objects.filter(
            problem=problem, language=language)

        # Get the list of the owners who have solutions for this problem and language
        owners = User.objects.filter(
            id__in=solutions.values_list("owner", flat=True))

        # Get current owner id from the owner form-select (if none selected take the first owner from owners)
        # owner_id = self.request.GET.get("owner", owners.first().id)
        owner_id = owners.first().id

        # Get owner from owner id.
        owner = get_object_or_404(User, id=owner_id)

        # Get all languages for the problem for curent owner
        solution_languages = Language.objects.filter(
            id__in=Solution.objects.filter(
                problem=problem, owner=owner).values_list("language", flat=True))

        # Get owners solution as queryset
        solutions = Solution.objects.filter(
            problem=problem, language=language, owner=owner)

        # There's only one solution per language per user
        solution = solutions.first()

        # Get related problems.
        common_tags = Count("tags", filter=Q(tags__in=problem.tags.all()))
        related_problems = (
            Problem.objects
            .annotate(common_tags=common_tags)
            .filter(common_tags__gte=2)
            .exclude(pk=problem.pk)
            .distinct()
        )

        # Output form
        output_form = OutputForm(initial={"output_area": "None from Views"})

        # Parse test cases
        test_cases = parse_test_cases(solution.test_case)

        # Parse URL
        url = parse_url(problem.url)

        context.update({
            "source_code": get_placeholder_source_code(language.id),
            "language": language,
            "language_id": language_id,
            "output_form": output_form,
            "owner_id": owner_id,
            "owners": owners,
            "related_problems": related_problems,
            "solution": solution,
            "solution_languages": solution_languages,  # Languages vailable in the dropdown
            "tag_list": problem.tags.all(),
            "test_cases": test_cases,
            "url": url,
        })
        return context


    def post(self, request, **kwargs):
        problem = self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        User = get_user_model()

        try:
            user_message = request.POST.get("message", "")
            # time.sleep(2)  # for tests
            # return JsonResponse({"response": "Waited 2 seconds."}) 
            if user_message:
                headers = {
                    "Authorization": f"Bearer {COHERE_API_KEY}",
                    "Content-Type": "application/json",
                }
                data = {
                    "model": "command",
                    "prompt": user_message,
                }

                response = requests.post("https://api.cohere.ai/v2/generate", json=data, headers=headers)

                if response.status_code != 200:
                    return JsonResponse({"error": f"API Error: {response.text}"}, status=response.status_code)

                ai_response = response.json()["generations"][0]["text"]
                return JsonResponse({"response": ai_response})

        except Exception as e:
            error_message = str(e)
            # print(f"AI Assistant Error: {error_message}")
            return JsonResponse({"error": error_message}, status=500)


        # If language is selected, update the URL
        language_id = request.POST.get("language")
        if language_id:
            language = get_object_or_404(Language, id=language_id)
            return redirect("python_problems:problem-detail", problem.slug, language.name)

        # Get owner from form select or keep the current one
        owner_id = int(request.POST.get("owner_id", context["owner_id"]))
        owner = get_object_or_404(User, id=owner_id)

        # Use the current language.
        language_id = context["language_id"]
        language = get_object_or_404(Language, id=language_id)

        solution = Solution.objects.filter(
            problem=problem,
            owner=owner,
            language=language).first()

        # judge0
        output_form = context["output_form"]
        source_code = request.POST.get("code_container")
        if source_code:
            code_executed = execute_code_by_judge0(source_code, language.name)
            output_form = OutputForm(
                initial={"output_area": code_executed})
        else:
            source_code = context["source_code"]

        context.update({
            "source_code": source_code,
            "language_id": language_id,
            "output_form": output_form,
            "owner_id": owner_id,
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
    form_class = SolutionForm  # Custom form to remove "owner" field.
    success_url = reverse_lazy('python_problems:problem-index')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super().form_valid(form)


class SolutionUpdate(LoginRequiredMixin, UpdateView):
    model = Solution
    form_class = SolutionForm  # Custom form to remove "owner" field.
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
