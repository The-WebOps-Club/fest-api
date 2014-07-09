import HTMLParser
from django.utils.html import strip_tags

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from apps.walls.utils import query_notifs, query_newsfeed,get_my_walls,get_my_posts
from apps.walls.models import Wall
from apps.api.serializers import *

class NotificationViewSet(viewsets.ViewSet):
    """
        Return notifications to an authenticated User
        page -- Start page number, Int
        limit -- number of items in each page: Int
        type --  type of notification: read, unread, all
    """
    def list(self, request):
        page = int(request.QUERY_PARAMS.get('page', 1))
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
		wallserializer=WallSerializer(walls,many=True)
	        return Response(wallserializer.data)



class PostsViewSet(viewsets.ViewSet):
	def list(self,request):
		wall_id = request.QUERY_PARAMS.get('id')
		if(wall_id==None):
			return Response({"error":"enter wall id"})		
		wall= Wall.objects.filter(id=wall_id)				
		posts = get_my_posts(request.user,wall)
		postserializer = PostSerializer(posts,many=True)
		for i in range(len(postserializer.data)):
			postserializer.data[i]["description"]=HTMLParser.HTMLParser().unescape(strip_tags(postserializer.data[i]["description"].strip()))

		return Response(postserializer.data)
			






