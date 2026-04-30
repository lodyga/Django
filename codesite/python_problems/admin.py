from django.contrib import admin
from .models import (
    Tag,
    Problem,
    Difficulty,
    Complexity,
    Solution,
    Language,
    TestCase,
)

admin.site.register(Tag)
admin.site.register(Difficulty)
admin.site.register(Complexity)
admin.site.register(Solution)
admin.site.register(Language)
admin.site.register(TestCase)


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    inlines = [TestCaseInline]
