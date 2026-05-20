import json
from django import forms
from django.core.exceptions import ValidationError
from .models import Problem, Solution, ProblemTestCase, ProblemType


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
            'One JSON test case per line. Either raw data, e.g. '
            '{"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]}, '
            'or linked-list payload with cycle metadata, e.g. '
            '{"inputs": [{"values": [3, 2, 0, -4], "cycle_position": 1}], "expected": true}, '
            'or object with attributes, e.g. '
            '{"data": {"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]}, "is_hidden": false, "explanation": ""}'
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
            "metadata",
            "problem_type",
            "method_name",
            "argument_names",
            "comparison_type",
        ]

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self._set_problem_type_dependent_fields()

        if self.instance.pk and self.instance.argument_names:
            self.initial["argument_names"] = json.dumps(
                self.instance.argument_names
            )

        if self.instance.pk:
            shared_test_cases = self.instance.get_shared_testcases(
                include_hidden=True
            )
            if self.current_user and self.current_user.is_authenticated:
                shared_test_cases = shared_test_cases.filter(
                    owner=self.current_user
                )

            self.fields["shared_test_cases"].initial = "\n".join(
                json.dumps({
                    "data": test_case.data,
                    "is_hidden": test_case.is_hidden,
                    "explanation": test_case.explanation,
                })
                for test_case in shared_test_cases
            )

    def _set_problem_type_dependent_fields(self):
        problem_type = (
            self.data.get("problem_type")
            if self.is_bound
            else self.initial.get("problem_type", self.instance.problem_type)
        )
        should_disable = problem_type == ProblemType.CLASS

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

            if (not isinstance(data, list) and not isinstance(data, dict)):
                raise ValidationError(
                    f"Line {index} must be a JSON list or object."
                )

            # Backward compatible format: raw test case payload as list/dict.
            if isinstance(data, list) or "data" not in data:
                parsed_test_cases.append({
                    "data": data,
                    "is_hidden": False,
                    "explanation": "",
                })
                continue

            test_case_data = data.get("data")
            is_hidden = data.get("is_hidden", False)
            explanation = data.get("explanation", "")

            if not isinstance(test_case_data, (list, dict)):
                raise ValidationError(
                    f"Line {index} key `data` must be a JSON list or object."
                )
            if not isinstance(is_hidden, bool):
                raise ValidationError(
                    f"Line {index} key `is_hidden` must be true/false."
                )
            if not isinstance(explanation, str):
                raise ValidationError(
                    f"Line {index} key `explanation` must be a string."
                )

            parsed_test_cases.append({
                "data": test_case_data,
                "is_hidden": is_hidden,
                "explanation": explanation,
            })

        return parsed_test_cases

    def clean_argument_names(self):
        if self.cleaned_data.get("problem_type") == ProblemType.CLASS:
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
            raise ValidationError(
                "Each argument name must be a non-empty string.")

        return argument_names

    def clean_method_name(self):
        if self.cleaned_data.get("problem_type") == ProblemType.CLASS:
            return ""

        method_name = self.cleaned_data.get("method_name")
        if not method_name:
            return ""

        return method_name

    def save(self, commit=True):
        parsed_test_cases = self.cleaned_data.get("shared_test_cases", [])
        problem = super().save(commit=commit)

        if commit:
            test_case_owner = self.current_user or problem.owner
            if not test_case_owner:
                raise ValidationError("Problem owner is required to save test cases.")

            problem.testcases.filter(owner=test_case_owner).delete()
            ProblemTestCase.objects.bulk_create([
                ProblemTestCase(
                    problem=problem,
                    owner=test_case_owner,
                    data=test_case_payload["data"],
                    is_hidden=test_case_payload["is_hidden"],
                    explanation=test_case_payload["explanation"],
                    order=index,
                )
                for index, test_case_payload in enumerate(parsed_test_cases, start=1)
            ])
        else:
            self._pending_shared_test_cases = parsed_test_cases

        return problem


class SolutionForm(forms.ModelForm):
    source_code = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 20}),
    )


class SolutionCreateForm(SolutionForm):
    class Meta:
        model = Solution
        exclude = ["owner", "test_cases"]


class SolutionUpdateForm(SolutionForm):
    class Meta:
        model = Solution
        exclude = ["problem", "language", "owner", "test_cases"]


class ProblemTestCaseCreateForm(forms.ModelForm):
    class Meta:
        model = ProblemTestCase
        fields = ["problem", "data", "is_hidden", "order", "explanation"]


class ProblemTestCaseUpdateForm(forms.ModelForm):
    class Meta:
        model = ProblemTestCase
        fields = ["problem", "data", "is_hidden", "order", "explanation"]
