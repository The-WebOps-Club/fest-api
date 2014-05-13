from django import template
from django.template.defaultfilters import stringfilter
from django.http.request import QueryDict
#from BeautifulSoup import BeautifulSoup, NavigableString
register = template.Library()

@register.filter(name="unread_by_wall")
def unread_by_wall(value, wid):
	count = 0
	for i in value.notifications.unread():
		if (i.target.wall.id == wid):
			count+=1

	return count
