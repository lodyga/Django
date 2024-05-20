import multiprocessing

from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Tag, Problem, Difficulty
from .forms import CodeForm, OutputForm


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

        if difficulty_id:
            problem_list = problem_list.filter(difficulty__id=difficulty_id)

        if query:
            problem_list = problem_list.filter(
                Q(tags__name__icontains=query) | Q(title__icontains=query)).distinct()

        problems_per_page = self.request.GET.get("problems_per_page", "10")

        paginator = Paginator(problem_list, problems_per_page)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context["problem_list"] = problem_list
        context["query"] = query
        context["difficulty_list"] = difficulty_list
        context["difficulty_id"] = difficulty_id
        context["page_obj"] = page_obj
        context["problems_per_page"] = problems_per_page
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
    template_name = "python_problems/problem_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        problem = self.get_object()
        related_problems = Problem.objects.filter(
            tags__in=problem.tags.all()).exclude(pk=problem.pk).distinct()
        
        code = """# Write code here.
# Remember to pass the solution to the output.

def fun(x):
    return x

output = fun(1)"""

        output_form = OutputForm(initial={"output_area": "None"})

        context["tags"] = problem.tags.values_list("name", flat=True)
        context["related_problems"] = related_problems
        context["output_form"] = output_form
        context["code_text"] = code
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Ensure self.object is set
        context = self.get_context_data(**kwargs)

        code = request.POST.get('code_area')
        try:
            result = execute_code(code)
            output_form = OutputForm(initial={"output_area": result})
        except Exception as e:
            output_form = OutputForm(initial={"output_area": f"Error: {str(e)}"})

        context["output_form"] = output_form
        context["code_text"] = code
        
        return self.render_to_response(context)


def execute_code(code):
    # Define a function to execute the code
    def code_execution(code, result_queue):
        local_vars = {}
        global_vars = {}
        try:
            exec(code, global_vars, local_vars)
            # result_queue.put(local_vars.get("output"))
            result_queue.put(local_vars["output"])
        except Exception as e:
            result_queue.put(f"Error: {str(e)}")

    # Create a multiprocessing Queue to receive the result from the child process
    result_queue = multiprocessing.Queue()

    # Create a child process to execute the code
    process = multiprocessing.Process(
        target=code_execution, args=(code, result_queue))

    try:
        # Start the child process
        process.start()

        # Wait for the process to finish or timeout after 10 seconds
        process.join(timeout=5)

        # Check if the process is still alive (i.e., if it timed out)
        if process.is_alive():
            # Terminate the process if it's still running
            process.terminate()
            process.join()

            # Return an error message indicating timeout
            return "Error: Execution timed out"

        # Retrieve the result from the Queue
        result = result_queue.get()

        return result
    finally:
        # Ensure that the child process is terminated
        if process.is_alive():
            process.terminate()
            process.join()


# same as ProblemDetailView
def problem_detail_view(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    related_problems = Problem.objects.filter(
        tags__in=problem.tags.all()).exclude(pk=pk).distinct()
    # code_form = CodeForm(initial={"code_area": "Some"})
    output_form = OutputForm(initial={"output_area": "None"})

    context = {
        "problem": problem,
        "tags": problem.tags.values_list("name", flat=True),
        "related_problems": related_problems,
        "output_form": output_form,
    }

    code = """# Write code here.
# Remember to pass the solution to the output.

def fun(x):
    return x

output = fun(1)"""

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
