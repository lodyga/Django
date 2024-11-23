from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .models import Tag, Difficulty, Complexity, Language, Problem, Solution
from .forms import OutputForm, ProblemForm, SolutionForm
from .static.python_problems.scripts import execute_code, parse_testcases, parse_url
from django.conf import settings

# REST API
from rest_framework import viewsets
from .serializers import TagSerializer, DifficultySerializer, ComplexitySerializer, LanguageSerializer, ProblemSerializer, SolutionSerializer


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

        # Context
        context["problem_list"] = problem_list
        context["difficulty_list"] = difficulty_list
        context["tag_list"] = tag_list
        context["query"] = query
        context["difficulty_id"] = difficulty_id
        context["order_by"] = order_by
        context["problems_per_page"] = problems_per_page
        context["page_obj"] = page_obj
        context["problem_languages"] = problem_languages

        return context


class ProblemDetailView(DetailView):
    model = Problem

    def get_context_data(self, **kwargs):
        # fetch get_context_data() from DetailView
        context = super().get_context_data(**kwargs)

        # fetch current problem
        problem = self.get_object()

        # capture language name from self.kwars which are captured from URL path
        language_name = self.kwargs.get("language")
        # fetch the language model  # Language.objects.get(name="Python")
        language = get_object_or_404(Language, name=language_name)
        # fetch solutions from all users based on the problem and the language
        solutions = Solution.objects.filter(
            problem=problem, language=language)

        # Fetch the list of the owners who have solutions for this problem and language
        owners = get_user_model().objects.filter(
            id__in=solutions.values_list("owner", flat=True))

        # Fetch the owner id from the owner form (if none take the first owner from owners)
        selected_owner_id = self.request.GET.get("owner", owners.first().id)

        # Fetch owner from owrer id.
        owner = get_object_or_404(
            get_user_model(), id=selected_owner_id)

        # Fetch owner solution as queryset
        solutions = Solution.objects.filter(
            problem=problem, language=language, owner=owner)

        # There's only one solution per language per user
        solution = solutions.first()

        # Fetch related problems.
        related_problems = Problem.objects.annotate(
            common_tags=Count("tags", filter=Q(tags__in=problem.tags.all()))
        ).filter(common_tags__gte=2).exclude(pk=problem.pk).distinct()

        # Default text for coding form.
        code_text = """# Write code here.\n# Remember to pass the solution to the output.\n\ndef fun(x):\n    return x\n\noutput = fun(1)"""

        # Output form
        output_form = OutputForm(initial={"output_area": "None"})

        # Parse testcases
        testcases, testcases_input, testcases_output = parse_testcases(
            solution.testcase)
        
        # Parse URL
        url = parse_url(problem.url)

        # Context
        context['owners'] = owners
        context['selected_owner'] = selected_owner_id
        context['solution'] = solution
        context["tags"] = problem.tags.values_list("name", flat=True)
        context["related_problems"] = related_problems
        context["code_text"] = code_text
        context["output_form"] = output_form
        context["testcases"] = testcases
        context["url"] = url

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)

        # Fetch code from a code area and execute it.
        code_text = request.POST.get("code_area")
        
        try:
            executed_code = execute_code(code_text)
            output_form = OutputForm(initial={"output_area": executed_code})
        except Exception as e:
            output_form = OutputForm(
                initial={"output_area": f"Error: {str(e)}"})

        # Context
        context["code_text"] = code_text
        context["output_form"] = output_form

        return self.render_to_response(context)


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
