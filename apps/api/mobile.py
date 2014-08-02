import HTMLParser
import urllib
from django.utils.html import strip_tags

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from apps.walls.utils import query_notifs, query_newsfeed,get_my_walls,get_my_posts,get_comments
from apps.walls.models import Wall,Post
from apps.api.serializers import *
from apps.walls.ajax import create_post
from apps.api.utils import *

class NotificationViewSet(viewsets.ViewSet):
	"""
		Return Notifications to an authenticated User
		page -- Start page number
		limit -- number of items in each page
		type --  type of notification
	"""
	def list(self, request):
		page = int(request.QUERY_PARAMS.get('page', 0))
		limit = int(request.QUERY_PARAMS.get('limit', 10))
		notif_type = request.QUERY_PARAMS.get('type', 'all')
		return Response(response_notificationviewset(request,notif_type,page,limit))

	# Standard API methods. Kept for future reference
	#def create(self, request):
	#    pass

	#def retrieve(self, request, pk=None):
	#    pass

	#def update(self, request, pk=None):
	#    pass

	#def partial_update(self, request, pk=None):
	#    pass

	#def destroy(self, request, pk=None):
	#    pass

class WallsViewSet(viewsets.ViewSet):
	
	def list(self,request):
		return Response(response_wallsviewset(request))



class PostsViewSet(viewsets.ViewSet):
	def list(self,request):
		wall_id=request.QUERY_PARAMS.get('wall_id')
		offset=request.QUERY_PARAMS.get('offset')
		limit=request.QUERY_PARAMS.get('limit')
		return Response(response_postviewset(request,wall_id,offset,limit))
	
	def create(self,request):
		wall_id=request.QUERY_PARAMS.get('wall_id')
		post=request.POST
		post=urllib.urlencode(post,True)
		created=create_post(request,wall_id,post)
		if created:
			return Response('created')
		else:
			return Response('not created')
	#def delete(self,request):
	#	pass

class CommentsViewSet(viewsets.ViewSet):
	def list(self,request):
		post_id=request.QUERY_PARAMS.get('post_id')
		offset=request.QUERY_PARAMS.get('offset')
		limit=request.QUERY_PARAMS.get('limit')
		return Response(response_commentviewset(request,post_id,offset,limit))		




