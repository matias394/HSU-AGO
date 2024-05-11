from django import template
from datetime import datetime

register = template.Library()

@register.filter
def iso_to_datetime(value):
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return value