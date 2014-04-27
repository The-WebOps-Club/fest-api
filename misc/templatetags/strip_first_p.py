from django import template
from django.template.defaultfilters import stringfilter
from django.http.request import QueryDict
from BeautifulSoup import BeautifulSoup, NavigableString
from django.utils.html import (conditional_escape, escapejs, fix_ampersands,
    escape, urlize as urlize_impl, linebreaks, strip_tags, avoid_wrapping)
register = template.Library()

@register.filter(name="strip_first_p", is_safe=True)
@stringfilter
def strip_first_p(value):
    soup = BeautifulSoup(value)
    soup.p.replaceWithChildren()
    return soup