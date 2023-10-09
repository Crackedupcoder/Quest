from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import strip_tags

register = template.Library()

@register.filter
def truncate_chars(value, max_length):
    if len(value) > max_length:
        return value[:max_length] + "..."
    return value



@register.filter(is_safe=True)
@stringfilter
def truncatechars_html(value, arg):
    """
    Truncate a string after a certain number of characters while preserving HTML tags.
    """
    length = int(arg)
    if len(value) <= length:
        return value
    truncated_text = value[:length]
    # Find the position of the last closing HTML tag
    last_tag_index = truncated_text.rfind('>')
    if last_tag_index == -1:
        return value
    # Strip any unclosed tags and add an ellipsis
    return truncated_text[:last_tag_index + 1] + '...'
