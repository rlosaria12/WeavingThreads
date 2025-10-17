from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get dictionary value by key safely."""
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def to(value, end):
    """Usage: {% for i in 2021|to:2035 %}"""
    return range(int(value), int(end) + 1)
