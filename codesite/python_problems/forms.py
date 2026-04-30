import json

from django import forms
from django.core.exceptions import ValidationError

from .models import Problem, Solution, TestCase


class ProblemForm(forms.ModelForm):
    argument_names = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
        help_text='Optional JSON list of argument names. Example: ["nums", "target"]',
    )
    shared_test_cases = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 8}),
        help_text=(
            'One JSON test case per line. Example: '
            '{"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]}'
        ),
        label="Test cases",
    )

    class Meta:
        model = Problem
        fields = [
            "title",
            "url",
            "difficulty",
            "description",
            "tags",
            "problem_type",
            "method_name",
            "argument_names",
        ]
        # exclude = ["slug", "owner"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._set_problem_type_dependent_fields()

        if self.instance.pk and self.instance.argument_names:
            self.initial["argument_names"] = json.dumps(
                self.instance.argument_names
            )

        if self.instance.pk:
            self.fields["shared_test_cases"].initial = "\n".join(
                json.dumps(test_case.data)
                for test_case in self.instance.get_shared_testcases(
                    include_hidden=True
                )
            )

    def _set_problem_type_dependent_fields(self):
        problem_type = (
            self.data.get("problem_type")
            if self.is_bound
            else self.initial.get("problem_type", self.instance.problem_type)
        )
        should_disable = problem_type == Problem.CLASS

        for field_name in ("method_name", "argument_names"):
            if should_disable:
                self.fields[field_name].widget.attrs["disabled"] = "disabled"
            else:
                self.fields[field_name].widget.attrs.pop("disabled", None)

    def clean_shared_test_cases(self):
        raw_value = self.cleaned_data.get("shared_test_cases", "")
        lines = [line.strip()
                 for line in raw_value.splitlines() 
                 if line.strip()]

        parsed_test_cases = []
        for index, line in enumerate(lines, start=1):
            try:
                data = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValidationError(
                    f"Line {index} is not valid JSON: {exc.msg}"
                ) from exc

            if not isinstance(data, dict):
                raise ValidationError(
                    f"Line {index} must be a JSON object."
                )

            # if "inputs" not in data or "expected" not in data:
            #     raise ValidationError(
            #         f'Line {index} must contain both "inputs" and "expected".'
            #     )

            parsed_test_cases.append(data)

        return parsed_test_cases

    def clean_argument_names(self):
        if self.cleaned_data.get("problem_type") == Problem.CLASS:
            return None

        raw_value = self.cleaned_data.get("argument_names", "").strip()
        if not raw_value:
            return None

        try:
            argument_names = json.loads(raw_value)
        except json.JSONDecodeError as exc:
            raise ValidationError(
                f'Argument names must be valid JSON: {exc.msg}'
            ) from exc

        if not isinstance(argument_names, list):
            raise ValidationError("Argument names must be a JSON list.")

        if not all(isinstance(name, str) and name.strip() for name in argument_names):
            raise ValidationError("Each argument name must be a non-empty string.")

        return argument_names

    def clean_method_name(self):
        if self.cleaned_data.get("problem_type") == Problem.CLASS:
            return None

        method_name = self.cleaned_data.get("method_name")
        if not method_name:
            return None

        return method_name

    def save(self, commit=True):
        parsed_test_cases = self.cleaned_data.get("shared_test_cases", [])
        problem = super().save(commit=commit)

        if commit:
            problem.testcases.all().delete()
            TestCase.objects.bulk_create([
                TestCase(problem=problem, data=data, order=index)
                for index, data in enumerate(parsed_test_cases, start=1)
            ])
        else:
            self._pending_shared_test_cases = parsed_test_cases

        return problem


class SolutionCreateForm(forms.ModelForm):
    class Meta:
        model = Solution
        exclude = ["owner"]


class SolutionUpdateForm(forms.ModelForm):
    class Meta:
        model = Solution
        exclude = ["problem", "language", "owner"]
