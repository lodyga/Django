from django.shortcuts import render
from python_problems.models import Language
from django.views.generic import TemplateView
from .scripts import *


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language_order = [
            "Python",
            "JavaScript",
            "Java",
            "C++",
            "Pandas",
            "MySQL",
            "PostgreSQL",
        ]
        languages = Language.objects.filter(name__in=language_order)
        languages_by_name = {language.name: language for language in languages}
        context["languages"] = [
            languages_by_name[name]
            for name in language_order
            if name in languages_by_name
        ]
        return context

    def post(self, request, **kwargs):
        if "message" in request.POST:
            return get_cohere_response(request)


def contact_view(request):
    return render(request, "core/contact.html")
