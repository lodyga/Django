from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.core.paginator import Paginator

from .models import Tag, Problem, Difficulty
from .forms import CodeForm, OutputForm, TestCaseForm, TestCaseInputForm, TestCaseOutputForm, ProblemForm
from .static.python_problems.scripts import execute_code


def tag_graph_view(request):
    tags = Tag.objects.all()
    data = [{'tag': tag.name, 'count': tag.problem_set.count()}
            for tag in tags]
    sorted_data = sorted(data, key=lambda x: x['count'], reverse=True)
    return render(request, 'python_problems/tag_graph.html', {'data': sorted_data})


class ProblemIndexView(ListView):
    model = Problem

    def get_context_data(self, **kwargs):
        context = super(ProblemIndexView, self).get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        problem_list = self.model.objects.all()
        difficulty_list = Difficulty.objects.all()
        difficulty_id = self.request.GET.get('difficulty', '')
        order_by = self.request.GET.get('order_by', 'created_at')

        if difficulty_id:
            problem_list = problem_list.filter(difficulty__id=difficulty_id)

        if query:
            problem_list = problem_list.filter(
                Q(tags__name__icontains=query) | Q(title__icontains=query)).distinct()

        problem_list = problem_list.order_by(order_by)

        # pagination
        problems_per_page = self.request.GET.get("problems_per_page", "10")

        paginator = Paginator(problem_list, problems_per_page)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        # context
        context["problem_list"] = problem_list
        context["query"] = query
        context["difficulty_list"] = difficulty_list
        context["difficulty_id"] = difficulty_id
        context["page_obj"] = page_obj
        context["problems_per_page"] = problems_per_page
        context["order_by"] = order_by

        return context


def problem_index_view(request):
    query = request.GET.get("query", "")
    problem_list = Problem.objects.all()
    difficulty_list = Difficulty.objects.all()
    difficulty_id = request.GET.get('difficulty', "")

    if difficulty_id:
        problem_list = problem_list.filter(difficulty__id=difficulty_id)

    if query:
        problem_list = problem_list.filter(
            Q(tags__name__icontains=query) | Q(title__icontains=query)).distinct()

    problems_per_page = request.GET.get("problems_per_page", "10")
    # try:
    #     problems_per_page = int(problems_per_page)
    # except ValueError:
    #     problems_per_page = 10

    paginator = Paginator(problem_list, problems_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "problem_list": problem_list,
        "query": query,
        "difficulty_list": difficulty_list,
        "difficulty_id": difficulty_id,
        'page_obj': page_obj,
        'problems_per_page': problems_per_page,
    }
    return render(request, "python_problems/problem_list.html", context)


class ProblemDetailView(DetailView):
    model = Problem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        problem = self.get_object()
        related_problems = Problem.objects.annotate(
            common_tags=Count('tags', filter=Q(tags__in=problem.tags.all()))
        ).filter(common_tags__gte=2).exclude(pk=problem.pk).distinct()

        code = """# Write code here.\n# Remember to pass the solution to the output.\n\ndef fun(x):\n    return x\n\noutput = fun(1)"""

        output_form = OutputForm(initial={"output_area": "None"})
        testcase_form = TestCaseForm()

        # testcases parsing
        # Split the test cases by newline characters
        if problem.testcase:
            raw_testcases = problem.testcase.split('\r\n')
        else:
            raw_testcases = "'), '"
        testcases = []
        testcases_input = []
        testcases_output = []
        for raw_testcase in raw_testcases:
            try:
                input_part, output_part = raw_testcase.split('), ')
                # Add the closing parenthesis back and remove opening parenthetis
                input_part = (input_part + ')').strip()[1:]
                # Strip any extra whitespace and closing parenthensi
                output_part = output_part.strip()[:-1]
            except:
                input_part = "Invalid testcase"
                output_part = "Invalid testcase"
            finally:
                testcases.append((input_part, output_part))
                testcases_input.append(input_part)
                testcases_output.append(output_part)


        testcase_input_form = TestCaseInputForm(
            initial={"testcase_input": testcases_input[0]})
        testcase_output_form = TestCaseOutputForm(
            initial={"testcase_output": testcases_output[0]})

        context["tags"] = problem.tags.values_list("name", flat=True)
        context["related_problems"] = related_problems
        context["output_form"] = output_form
        context["code_text"] = code

        context["testcases"] = testcases
        context["testcase_form"] = testcase_form
        context["testcase_input_form"] = testcase_input_form
        context["testcase_output_form"] = testcase_output_form
        context["testcases_input"] = testcases_input
        context["testcases_output"] = testcases_output

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Ensure self.object is set
        context = self.get_context_data(**kwargs)

        code = request.POST.get('code_area')
        try:
            result = execute_code(code)
            output_form = OutputForm(initial={"output_area": result})
        except Exception as e:
            output_form = OutputForm(
                initial={"output_area": f"Error: {str(e)}"})

        context["output_form"] = output_form
        context["code_text"] = code

        return self.render_to_response(context)


# same as ProblemDetailView
def problem_detail_view(request, slug):
    problem = get_object_or_404(Problem, slug=slug)
    related_problems = Problem.objects.filter(
        tags__in=problem.tags.all()).exclude(slug=slug).distinct()
    # code_form = CodeForm(initial={"code_area": "Some"})
    output_form = OutputForm(initial={"output_area": "None"})

    context = {
        "problem": problem,
        "tags": problem.tags.values_list("name", flat=True),
        "related_problems": related_problems,
        "output_form": output_form,
    }

    code = """# Write code here.\n# Remember to pass the solution to the output.\n\ndef fun(x):\n    return x\n\noutput = fun(1)"""

    if request.method == 'POST':
        code = request.POST.get('code_area')
        # code_form = CodeForm(initial={'code_area': code})

        try:
            result = execute_code(code)
            output_form = OutputForm(initial={"output_area": result})
        except Exception as e:
            output_form = OutputForm(
                initial={"output_area": f"Error: {str(e)}"})

    # context["code_form"] = code_form
    context["output_form"] = output_form
    context["code_text"] = code
    # print(output_form.initial.get("output_area"))
    # print(output_form.initial["output_area"])
    # print(output_form["output_area"].value())

    # print(dir(output_form))
    # print(output_form.__dict__)
    # print(output_form.__dict__.get("initial").get("output_area"))
    # print(output_form.fields.get("output_area").widget.attrs.get("placeholder"))

    return render(request, "python_problems/problem_detail.html", context)


"""
print(output_form.__dict__):
{'is_bound': False, 'data': <MultiValueDict: {}>, 'files': <MultiValueDict: {}>, 'auto_id': 'id_%s', 'initial': {'output_area': "Error: 'output'"}, 'error_class': <class 'django.forms.utils.ErrorList'>, 'label_suffix': ':', 'empty_permitted': False, '_errors': None, 'fields': {'output_area': <django.forms.fields.CharField object at 0x7832c705b1f0>}, '_bound_fields_cache': {}, 'renderer': <django.forms.renderers.DjangoTemplates object at 0x7832c701b0a0>}

"""


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
    form_class = ProblemForm  # Custom form to remove 'slug' field
    success_url = reverse_lazy('python_problems:index')


class ProblemUpdate(LoginRequiredMixin, UpdateView):
    model = Problem
    fields = "__all__"
    success_url = reverse_lazy('python_problems:index')


class ProblemDelete(LoginRequiredMixin, DeleteView):
    model = Problem
    fields = "__all__"
    success_url = reverse_lazy('python_problems:index')
