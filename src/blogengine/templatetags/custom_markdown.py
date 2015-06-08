import markdown2 as markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def custom_markdown(value):
    extras = ["fenced-code-blocks"]

    return mark_safe(markdown.markdown(force_unicode(value),
                                        extras = extras))
