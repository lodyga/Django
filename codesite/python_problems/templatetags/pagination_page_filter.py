from django import template

register = template.Library()


@register.filter
def in_pagination_range(page_number, page_obj):
    return (
        page_number > page_obj.number - 4 and  # span starts
        page_number < page_obj.number + 4 or  # span ends
        page_number < 4 or  # first 3 pages
        page_number > page_obj.paginator.num_pages - 3  # last 3 pages
    )
