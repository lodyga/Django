from django import forms
from .models import Problem, Solution


# Custom form to remove "slug", "owner" fields
class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        exclude = ["slug", "owner"]


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        exclude = ["owner"]

