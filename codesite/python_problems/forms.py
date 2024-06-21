from django import forms
from python_problems.models import Problem, Solution, Language


# Custom form to remove "slug", "owner" fields
class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        exclude = ["slug", "owner"]


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        exclude = ["owner"]


class OutputForm(forms.Form):
    output_area = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "None", 'rows': 3, 'cols': 80}))
