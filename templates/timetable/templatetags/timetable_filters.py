from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary using a key"""
    return dictionary.get(key, [])