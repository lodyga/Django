from django.contrib import admin

from .models import Tag, Problem, Difficulty

admin.site.register(Tag)
admin.site.register(Problem)
admin.site.register(Difficulty)
