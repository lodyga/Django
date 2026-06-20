import re
from python_problems.models import Problem, ProblemType


def get_problem_metadata(problem):
    if problem.metadata is None:
        raise ValueError("No metadata.")

    metadata = problem.metadata

    if "problem_type" not in metadata:
        raise ValueError("No problem type in metadata.")
    elif "comparison_type" not in metadata:
        raise ValueError("No problem type in metadata.")

    if metadata["problem_type"] == ProblemType.CLASS:
        if "class_name" not in metadata:
            raise ValueError("No class name in metadata.")
    else:
        if "method_name" not in metadata:
            raise ValueError("No method name in metadata.")
        elif "parameters" not in metadata:
            raise ValueError("No parameters in metadata.")
        elif "return_type" not in metadata:
            raise ValueError("No return type in metadata.")

    return metadata


def parse_url(raw_url):
    return re.search(r"((https?)://)?(www\.)?(app\.)?(\w+\.\w+)(/)?", raw_url).group(5)


def get_adjacent_slugs(problem):
    problem_list = Problem.objects.filter()

    problem_ids = list(problem_list.values_list("id", flat=True))

    problem_index = problem_ids.index(problem.id)

    prev_problem_id = problem_ids[problem_index - 1]

    next_problem_id = problem_ids[(problem_index + 1) % len(problem_ids)]

    prev_problem_slug = Problem.objects.filter(
        id=prev_problem_id).first().slug

    next_problem_slug = Problem.objects.filter(
        id=next_problem_id).first().slug

    return (prev_problem_slug, next_problem_slug)


def parse_problem_description(problem_description):
    if not problem_description:
        return ("", [])

    normalized = problem_description.replace("\r\n", "\n")

    def clean_segment(text):
        cleaned = re.sub(r"(?i)</?p>", "\n", text)
        cleaned = re.sub(r"(?i)<br\s*/?>", "\n", cleaned)
        cleaned = re.sub(r"(?i)</?b>", "", cleaned)
        lines = [line for line in cleaned.split("\n")]

        while lines and not lines[0]:
            lines.pop(0)
        while lines and not lines[-1]:
            lines.pop()

        if lines[0].startswith("Example "):
            lines.pop(0)
        return "\n".join(lines)

    pre_blocks = re.findall(r"(?is)<pre>(.*?)</pre>", normalized)
    question_raw = normalized.split(
        "<pre>", 1)[0] if pre_blocks else normalized

    question = clean_segment(question_raw)
    examples = []
    for block in pre_blocks:
        cleaned_block = clean_segment(block)
        if cleaned_block:
            examples.append(cleaned_block)

    return (question, examples)
