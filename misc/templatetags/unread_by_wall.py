from django import template
from django.template.defaultfilters import stringfilter
from django.http.request import QueryDict

register = template.Library()

@register.filter( name = "unread_by_wall" )
def unread_by_wall( value, wid ):
	return value.notifications.unread().filter( description__contains = 'wall:' + format( wid ) ).count();
