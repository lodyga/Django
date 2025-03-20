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


class OutputForm(forms.Form):
    output_area = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "None from Forms", "rows": 3, "cols": 80}))
