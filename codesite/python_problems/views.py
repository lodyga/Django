import multiprocessing

from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

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
        difficulty_id = self.request.GET.get('difficulty', 0)

        if difficulty_id:
            problem_list = problem_list.filter(difficulty__id=difficulty_id)

        if query:
            problem_list = problem_list.filter(
                Q(tags__name__icontains=query) | Q(title__icontains=query)).distinct()

        context["problem_list"] = problem_list
        context["query"] = query
        context["difficulty_list"] = difficulty_list
        context["difficulty_id"] = int(difficulty_id)
        return context


def problem_index_view(request):
    query = request.GET.get("query", "")
    problem_list = Problem.objects.all()
    difficulty_list = Difficulty.objects.all()
    difficulty_id = request.GET.get('difficulty', 0)

    if difficulty_id:
        problem_list = problem_list.filter(difficulty__id=difficulty_id)

    if query:
        problem_list = problem_list.filter(
            Q(tags__name__icontains=query) | Q(title__icontains=query)).distinct()

    context = {
        "problem_list": problem_list,
        "query": query,
        "difficulty_list": difficulty_list,
        "difficulty_id": int(difficulty_id),
    }
    return render(request, "python_problems/problem_list.html", context)


class ProblemDetailView(DetailView):
    model = Problem

    def get_context_data(self, **kwargs):
        context = super(ProblemDetailView, self).get_context_data(**kwargs)
        problem = self.get_object()
        context["tags"] = problem.tags.values_list("name", flat=True)
        context["related_problems"] = Problem.objects.filter(
            tags__in=problem.tags.all()).exclude(pk=problem.pk).distinct()
        return context


def execute_code(code):
    # Define a function to execute the code
    def code_execution(code, result_queue):
        local_vars = {}
        global_vars = {}
        try:
            exec(code, global_vars, local_vars)
            result_queue.put(local_vars.get("output"))
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

    context = {
        "problem": problem,
        "tags": problem.tags.values_list("name", flat=True),
        "related_problems": related_problems,
        "output_form": OutputForm(),
    }

    if request.method == 'POST':
        code = request.POST.get('code_area')
        # print(code) # output = 20
        code_form = CodeForm(initial={'code_area': code})
        # print(code_form) # <tr>
        
        try:
            result = execute_code(code)
            output_form = OutputForm(initial={"output_area": result})
            context["output_form"] = output_form
        except Exception as e:
            output_form = OutputForm(
                initial={"output_area": f"Error: {str(e)}"})
            context["output_form"] = output_form
    else:
        code = ""
        
    context["code_form"] = code
    context["code_text"] = code
    return render(request, "python_problems/problem_detail.html", context)


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
