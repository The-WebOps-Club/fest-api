from django import template
from django.http.request import QueryDict
from BeautifulSoup import BeautifulSoup, NavigableString

register = template.Library()

@register.filter(name="strip_first_p")
def strip_first_p(value):
    soup = BeautifulSoup(value)
    for tag in soup.findAll(True):
        if tag.name == "p":
            s = ""
            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(unicode(c), invalid_tags)
                s += unicode(c)
            tag.replaceWith(s)
            break
    print soup
    return soup