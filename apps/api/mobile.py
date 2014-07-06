import HTMLParser
from django.utils.html import strip_tags

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from apps.walls.utils import query_newsfeed


class NotificationViewSet(viewsets.ViewSet):
    """
        method: GET
        params: 
            page: Start page number
            limit: number of items in each page
        authorization: Token
    """
    def list(self, request):
        page = int(request.GET['page'])
        limit = int(request.GET['limit'])
        newsfeed = query_newsfeed(request.user, page=page, max_items=limit)
        json = []
        for notif in newsfeed:
            item = {}
            item['id'] = notif.id
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
    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
