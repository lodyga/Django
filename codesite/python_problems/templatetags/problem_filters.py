from django import template

register = template.Library()


@register.filter
def dict_key(problem_languages, problem):
    return problem_languages.get(problem)
