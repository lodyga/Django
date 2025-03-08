from django.contrib import admin
from .models import Tag, Problem, Difficulty, Complexity, Solution, Language

admin.site.register(Tag)
admin.site.register(Problem)
admin.site.register(Difficulty)
admin.site.register(Complexity)
admin.site.register(Solution)
admin.site.register(Language)
