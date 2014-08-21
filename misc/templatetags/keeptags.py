
from django import template

#Tell django that this is a template filter module
register = template.Library()

def keeptags(value, tags):
    """
    Strips all [X]HTML tags except the space seperated list of tags 
    from the output.
    
    Usage: keeptags:"strong em ul li"
    """
    import re
    from django.utils.html import strip_tags, escape
    tags = [re.escape(tag) for tag in tags.split()]
    tags_re = '(%s)' % '|'.join(tags)
    singletag_re = re.compile(r'<(%s\s*/?)>' % tags_re)
    starttag_re = re.compile(r'<(%s)(\s+[^>]+)>' % tags_re)
    endtag_re = re.compile(r'<(/%s)>' % tags_re)
    value = singletag_re.sub('##~~~\g<1>~~~##', value)
    value = starttag_re.sub('##~~~\g<1>\g<3>~~~##', value)
    value = endtag_re.sub('##~~~\g<1>~~~##', value)
    value = strip_tags(value)
    value = escape(value)
    recreate_re = re.compile('##~~~([^~]+)~~~##')
    value = recreate_re.sub('<\g<1>>', value)
    return value
