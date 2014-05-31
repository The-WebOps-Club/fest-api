from django import template
from django.template.defaultfilters import stringfilter
from django.http.request import QueryDict
from apps.walls.utils import check_admin_access_rights
#from BeautifulSoup import BeautifulSoup, NavigableString
register = template.Library()

@register.filter(name="check_access")
def check_access( user , post ):
	#import pdb;pdb.set_trace();
	if check_admin_access_rights( user, post ):
		return True
	else:
		return False