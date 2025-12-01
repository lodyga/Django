from django import forms
from .models import Problem, Solution


# Custom form to remove "slug", "owner" fields
class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ["title", "url", "difficulty", "tags", "description"]
        # exclude = ["slug", "owner"]


class SolutionCreateForm(forms.ModelForm):
    class Meta:
        model = Solution
        exclude = ["owner"]


class SolutionUpdateForm(forms.ModelForm):
    class Meta:
        model = Solution
        exclude = ["problem", "language", "owner"]

