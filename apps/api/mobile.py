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
		if notif_type == 'all':
			notifs = query_newsfeed(request.user, page=page, max_items=limit)
		else:
			notifs = query_notifs(request.user, page=page, max_items=limit, notif_type=notif_type)
		json = []
		for notif in notifs:
			item = {}
			item['id'] = notif.id
			item['unread'] = notif.unread
			item['actor'] = {}
			item['actor']['name'] = notif.actor.get_full_name()
			item['actor']['id'] = notif.actor.id
			item['verb'] = notif.verb
			item['wall'] = {}
			item['wall']['name'] = notif.target.wall.name
			item['wall']['id'] = notif.target.wall.id
			if notif.verb == "has commented on":
				target_type = "post"
				target_name = notif.target.subject
				target_id = notif.target.id
			elif notif.verb == "has posted on":
				target_type = "wall"
				target_name = item['wall']['name']
				target_id = item['wall']['id']
			item['target'] = {}
			item['target']['type'] = target_type 
			item['target']['name'] = target_name
			item['target']['id'] = target_id
			item['description'] = HTMLParser.HTMLParser().unescape(strip_tags(notif.action_object.description.strip()))
			item['timestamp'] = notif.timestamp
			json.append(item)
		return Response(json)

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
		walls = get_my_walls(request.user)
		if not walls :
			return Response({"error:no walls to be displayed"})
		wallserializer=WallSerializer(walls,many=True)
		return Response(wallserializer.data)



class PostsViewSet(viewsets.ViewSet):
	def list(self,request):
		wall_id=request.QUERY_PARAMS.get('wall_id')
		offset=request.QUERY_PARAMS.get('offset')
		limit=request.QUERY_PARAMS.get('limit')
		if not wall_id:
		   return Response({"error":"enter wall id"})
		wall= Wall.objects.filter(id=wall_id)
		if not wall:
			return Response({'error':'no wall with that id exists'})	
		posts = get_my_posts(request.user,wall,offset,limit)
		try:
			if posts['error']:
				return Response(posts)
		except:
			pass
		if not posts:
			return Response({"error":"no posts to be displayed"})		
		postserializer = PostSerializer(posts,many=True)
		for i in range(len(postserializer.data)):
			postserializer.data[i]["description"]=HTMLParser.HTMLParser().unescape(strip_tags(postserializer.data[i]["description"].strip()))
		return Response(postserializer.data)
	
	def create(self,request):
		wall_id=request.QUERY_PARAMS.get('wall_id')
		post=request.POST
		post=urllib.urlencode(post,True)
		create_post(request,wall_id,post)
		return Response('created')

	#def delete(self,request):
	#	pass

class CommentsViewSet(viewsets.ViewSet):
	def list(self,request):
		post_id=request.QUERY_PARAMS.get('post_id')
		offset=request.QUERY_PARAMS.get('offset')
		limit=request.QUERY_PARAMS.get('limit')
		if not post_id:
		   return Response({"error":"enter post id"})		
		post=Post.objects.filter(id=post_id)
		if not post:
			return Response({'error':'no post with that id exists'})
		print post
		comments = get_comments(request.user,post[0],offset,limit)
		if not comments:
			return Response({'error':'no comments to be displayed'})
		commentserializer=CommentSerializer(comments,many=True)
		for i in range(len(commentserializer.data)):
			commentserializer.data[i]["description"]=HTMLParser.HTMLParser().unescape(strip_tags(commentserializer.data[i]["description"].strip()))
		return Response(commentserializer.data)		




