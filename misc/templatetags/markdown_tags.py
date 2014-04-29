from django import template
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
import misc.markdown as markdown_render
from django.conf import settings

register = template.Library()

@register.filter(name="markdown")
def markdown_filter(value, style="default"):
    """Processes the given value as Markdown, optionally using a particular
    Markdown style/config

    Syntax::
        {{ value|markdown }}
        {{ value|markdown:"mystyle" }}
    """
    try:
        return mark_safe(markdown_render.markdown(value, style))
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in `markdown` filter: "
                "The python-markdown2 library isn't installed.")
        return force_unicode(value)
markdown_filter.is_safe = True
