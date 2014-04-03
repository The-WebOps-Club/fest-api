from django import template
from django.http.request import QueryDict

register = template.Library()

@register.tag(name="once")
def do_once(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, var_name = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    nodelist = parser.parse(('endonce',))
    parser.delete_first_token()
    return DoOnceNode(nodelist, var_name)

class DoOnceNode(template.Node):
    def __init__(self, nodelist, var_name):
        self.nodelist = nodelist
        self.var_name = '_do_once_'+var_name
    def render(self, context):
        request = context['request']

        # Make request.GET mutable.
        # request.GET = dict(request.GET)

        if self.var_name in request.GET:
            return ''
        else:
        	mydict = {self.var_name : 1}
        	qdict = QueryDict('')
        	qdict = request.GET.copy()
        	qdict.update(mydict)
        	request.GET = qdict
        	# request.GET[self.var_name] = 1
        	return self.nodelist.render(context)