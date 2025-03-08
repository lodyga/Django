from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import OutputForm, ProblemForm, SolutionForm
from .models import Complexity, Difficulty, Language, Problem, Solution, Tag
from .static.python_problems.scripts import execute_code, parse_testcases, parse_url

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
    tags = Tag.objects.all()
    data = [{'tag': tag.name, 'count': tag.problem_set.count()}
            for tag in tags]
    sorted_data = sorted(data, key=lambda x: x['count'], reverse=True)
    return render(request, 'python_problems/tag_graph.html', {'data': sorted_data})


class ProblemIndexView(ListView):
    model = Problem

    def get_context_data(self, **kwargs):
        # fetch get_context_data from parent class
        context = super().get_context_data(**kwargs)

        # Fetch data from database.
        problem_list = self.model.objects.all()
        difficulty_list = Difficulty.objects.all()
        tag_list = Tag.objects.all()

        # Fetch data from request.
        query = self.request.GET.get("query", "")
        difficulty_id = int(self.request.GET.get(
            "difficulty")) if self.request.GET.get("difficulty") else 0
        order_by = self.request.GET.get("order_by", "created_at")

        # Fileter problems by difficulty.
        if difficulty_id:
            problem_list = problem_list.filter(difficulty__id=difficulty_id)

        # Filter problems by query from search form.
        if query:
            problem_list = problem_list.filter(
                Q(tags__name__icontains=query) | Q(title__icontains=query)).distinct()

        # For each problem, get distinct language from solutions
        problem_languages = {
            problem: Language.objects.filter(
                id__in=Solution.objects.filter(problem=problem).values_list('language', flat=True).distinct())
            for problem in problem_list
        }

        # Order problems.
        problem_list = problem_list.order_by(order_by)

        # Pagination of problems.
        problems_per_page = int(self.request.GET.get("problems_per_page", 10))
        paginator = Paginator(problem_list, problems_per_page)
        page_number = self.request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        context.update({
            "problem_list": problem_list,
            "difficulty_list": difficulty_list,
            "tag_list": tag_list,
            "query": query,
            "difficulty_id": difficulty_id,
            "order_by": order_by,
            "problems_per_page": problems_per_page,
            "page_obj": page_obj,
            "problem_languages": problem_languages,
        })

        return context


class ProblemDetailView(DetailView):
    model = Problem
    template_name = "python_problems/problem_detail.html"  # needed for post render()
    default_code_text = """# Write code here.\r\n# Remember to pass the solution to the output.\r\n\r\ndef fun(x):\r\n    return x\r\n\r\noutput = fun(1)"""

    def get_context_data(self, **kwargs):
        User = get_user_model()

        # fetch get_context_data() from DetailView
        context = super().get_context_data(**kwargs)

        # get current problem
        problem = self.get_object()

        # Get current language from the URL
        language_name = self.kwargs.get("language")

        # get the language model  # Language.objects.get(name="Python")
        language = get_object_or_404(Language, name=language_name)
        del language_name

        # solution language id
        language_id = language.id

        # fetch solutions for all users based on the problem and the language
        solutions = Solution.objects.filter(
            problem=problem, language=language)

        # Fetch the list of the owners who have solutions for this problem and language
        owners = User.objects.filter(
            id__in=solutions.values_list("owner", flat=True))

        # Fetch current owner id from the owner form-select (if none selected take the first owner from owners)
        owner_id = self.request.GET.get("owner", owners.first().id)

        # Fetch owner from owner id.
        owner = get_object_or_404(User, id=owner_id)

        # Get all languages for the problem for curent owner
        solution_languages = Language.objects.filter(
            id__in=Solution.objects.filter(
                problem=problem, owner=owner).values_list("language", flat=True))

        # Fetch owner solution as queryset
        solutions = Solution.objects.filter(
            problem=problem, language=language, owner=owner)

        # There's only one solution per language per user
        solution = solutions.first()

        # Fetch related problems.
        related_problems = Problem.objects.annotate(
            common_tags=Count("tags", filter=Q(tags__in=problem.tags.all()))
        ).filter(common_tags__gte=2).exclude(pk=problem.pk).distinct()

        # Output form
        output_form = OutputForm(initial={"output_area": "None"})

        # Parse testcases
        testcases, testcases_input, testcases_output = parse_testcases(
            solution.testcase)

        # Parse URL
        url = parse_url(problem.url)

        context.update({
            "owners": owners,
            "owner_id": owner_id,
            "solution": solution,
            "language": language,  # Pass the selected language
            "language_id": language_id,  # Used for the <option> selected state
            "solution_languages": solution_languages,  # Available languages in the dropdown
            "tags": problem.tags.values_list("name", flat=True),
            "related_problems": related_problems,
            "code_text": self.default_code_text,
            "output_form": output_form,
            "testcases": testcases,
            "url": url,
        })

        return context

    def post(self, request, **kwargs):
        self.object = self.get_object()
        problem = self.object  # Get the Problem instance
        context = self.get_context_data(**kwargs)
        User = get_user_model()

        # If language is selected, update the URL
        language_id = request.POST.get("language")
        if language_id:
            language = get_object_or_404(Language, id=language_id)
            return redirect("python_problems:problem-detail", problem.slug, language.name)

        # Get code from a code area and execute it.
        code_text = request.POST.get("code_area")
        try:
            executed_code = execute_code(code_text)
            output_form = OutputForm(initial={"output_area": executed_code})
        except Exception as e:
            output_form = OutputForm(
                initial={"output_area": f"Error: {str(e)}"})

        # Get owner from form select or keep the current one
        owner_id = request.POST.get("owner") or context["owner_id"]
        owner = get_object_or_404(User, id=owner_id)

        # Use the current language.
        language_id = context["language_id"]
        language = get_object_or_404(Language, id=language_id)

        context.update({
            "code_text": self.default_code_text,
            "output_form": output_form,
            "owner_id": owner_id,
            "language_id": language_id,
            "solution": Solution.objects.filter(
                problem=problem, owner=owner, language=language).first()
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
