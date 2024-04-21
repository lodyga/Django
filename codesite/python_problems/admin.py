from django.contrib import admin

from .models import Tag
from .models import Problem

admin.site.register(Tag)
admin.site.register(Problem)
