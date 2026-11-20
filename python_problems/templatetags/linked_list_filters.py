from django import template
import re

register = template.Library()


@register.filter
def process_linked_lists(text):
    # Replace <linkedlist> tags with graphical versions
    return re.sub(
        r"<linkedlist>([^<]+)</linkedlist>",
        _convert_to_linked_list,
        text)


def _convert_to_linked_list(match):
    items = (item.strip()
             for item in match.group(1).split(",")
             if item.strip())
    if not items:
        return match.group(0)

    nodes = []
    for item in items:
        nodes.append(f'<div class="ll-node">{item}</div>')
        nodes.append('<div class="ll-arrow"></div>')

    return (
        f'<div class="linked-list-container">'
        f'{"".join(nodes)}'
        f'<span class="ll-null">NULL</span>'
        f"</div>")
