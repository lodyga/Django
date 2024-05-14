from django import forms


class CodeForm(forms.Form):
    code_area = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "Write a code", 'rows': 10, 'cols': 80}))
