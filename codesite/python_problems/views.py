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


# same as ProblemDetailView
def problem_detail_view(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    related_problems = Problem.objects.filter(
        tags__in=problem.tags.all()).exclude(pk=pk).distinct()

    context = {
        "problem": problem,
        "tags": problem.tags.values_list("name", flat=True),
        "related_problems": related_problems,
        "code_form": CodeForm(),
        "output_form": OutputForm(),
    }
    
    if request.method == 'POST':
        # context["is_code_area"] = True
        code = request.POST.get('code_area')

        # keep the code in code_form after submiting
        code_form = CodeForm(initial={'code_area': code})
        context["code_form"] = code_form


        try:
            local_vars = {}
            global_vars = {}
            # Execute the code
            exec(code, global_vars, local_vars)
            print(local_vars)
            # Get the result from the local variables dictionary
            result = local_vars.get("output", "non")

            # context["processed_code"] = result
            output_form = OutputForm(initial={"output_area": result})
            context["output_form"] = output_form
        except Exception as e:
            output_form = OutputForm(initial={"output_area": f"Error: {str(e)}"})
            context["output_form"] = output_form


        # output = None
        # local_vars = {'output': output}  # Pre-populate local_vars
        # try:
        #     exec(code, globals(), local_vars)
        #     output = local_vars['output']  # Capture output from local variable
        #     print(local_vars)
        #     context["processed_code"] = output
        # except Exception as e:
        #     output = f"Error: {str(e)}"


        # try:
        #     # Use exec to execute the code block
        #     namespace = {}
        #     # exec(code, namespace)
        #     # Retrieve the result from the namespace
        #     # result = namespace.get("some", None)
        #     # result = exec(code)
        #     result = exec(print("udpa"))
        #     print(result)
        #     context["processed_code"] = result
        # except Exception as e:
        #     context["processed_code"] = f"Error: {str(e)}"

#         try:
#             # Extract function body (assuming function is defined at the beginning)
#             # Extract function body components
#             function_body = code.splitlines()[0].split()[1:]
#             function_body = " ".join(function_body)  # Join back into a string
# 
#             # Directly evaluate the function body (risky, replace with safe execution)
#             # Dangerous, replace with safe execution
#             result = eval(f"def fun(x): {function_body}")
#             result = result(1)  # Call the function with argument
# 
#             # context = {'processed_code': result}
#             context["processed_code"] = result
#         except Exception as e:
#             # context = {'processed_code': f"Error: {str(e)}"}
#             context["processed_code"] = f"Error: {str(e)}"

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
