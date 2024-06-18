from django import forms
from python_problems.models import Problem


# Custom form to remove "slug", "owner" fields
class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        exclude = ["slug", "owner"]


class CodeForm(forms.Form):
    code_area = forms.CharField(widget=forms.Textarea())

#         attrs={"class": "python-code", 'rows': 10, 'cols': 80}
# , "placeholder": "#  Write code here.\n#  Remember to pass a solution to an ouput.\n\ndef fun(x):\n    return x\n\noutput = fun(1)"


class OutputForm(forms.Form):
    output_area = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "None", 'rows': 3, 'cols': 80}))


class TestCaseForm(forms.Form):
    testcase = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "None", 'rows': 6}))


class TestCaseInputForm(forms.Form):
    testcase_input = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "None", 'rows': 1}))


class TestCaseOutputForm(forms.Form):
    testcase_output = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "None", 'rows': 1}))
