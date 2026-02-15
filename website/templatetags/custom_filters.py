from django import template

register = template.Library()

@register.filter(name='split')
def split(value, separator=','):
    """Split a string by a separator"""
    if not value:
        return []
    return [item.strip() for item in str(value).split(separator)]
