from django import forms


class CodeForm(forms.Form):
    code_area = forms.CharField(widget=forms.Textarea(
        attrs={"class": "python-code", "placeholder": "#  Write code here.\n#  Remember to pass a solution to an ouput.\n\ndef fun(x):\n    return x\n\noutput = fun(1)", 'rows': 10, 'cols': 80}))


class OutputForm(forms.Form):
    output_area = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "None", 'rows': 5, 'cols': 80}))
