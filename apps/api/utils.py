import HTMLParser
import urllib
from django.utils.html import strip_tags

from apps.api.mobile import *
from apps.api.serializers import *
from apps.walls.utils import get_my_walls,get_my_posts,get_comments
from apps.walls.models import Wall,Post
from apps.api.serializers import *
def response_notificationviewset(request,notif_type,page,limit):
	temp={}
	temp['status']=0
	temp['message']='error'
	temp['data']=[]
	json=[]
	if notif_type == 'all':
		notifs = query_newsfeed(request.user, page=page, max_items=limit)
	else:
		notifs = query_notifs(request.user, page=page, max_items=limit, notif_type=notif_type)
	if not notifs:
		temp['message']='no notifications to be displayed'
		return temp
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
	temp['status']=1
	temp['message']='success'
	temp['data']=json
	return temp

def response_postviewset(request,wall_id=None,offset=0,limit=None):
	temp={}
	temp['status']=0
	temp['message']='error'
	temp['data']=[]
	if not wall_id:
		temp['message']='please enter wall id'
		return temp
	wall= Wall.objects.filter(id=wall_id)
	if not wall:
		temp['message']='no wall with that id exists'
		return temp
	posts = get_my_posts(request.user,wall,offset,limit)
	try:
		if posts['error']:
			temp['message']=posts['error']
			return temp
	except:
		pass
	if not posts:
		temp['message']='no post with that id exists'
		return temp
	postserializer = PostSerializer(posts,many=True)
	for i in range(len(postserializer.data)):
		postserializer.data[i]["description"]=HTMLParser.HTMLParser().unescape(strip_tags(postserializer.data[i]["description"].strip()))	
	temp['status']=1
	temp['message']='success'
	temp['data']=postserializer.data
	return temp

def response_wallsviewset(request):
	temp={}
	temp['status']=0
	temp['message']='error'
	temp['data']=[]
	walls = get_my_walls(request.user)
	if not walls :
		temp['message']='no walls to be displayed'
		return temp
	wallserializer=WallSerializer(walls,many=True)
	temp['data']=wallserializer.data
	temp['status']=1
	temp['message']='success'
	return temp

def response_commentviewset(request,post_id=None,offset=0,limit=None):
	temp={}
	temp['status']=0
	temp['message']='error'
	temp['data']=[]
	if not post_id:
	   temp['message']='please enter post id'
	   return temp	
	post=Post.objects.filter(id=post_id)
	if not post:
		temp['message']='no post with that id exists'
		return temp
	comments = get_comments(request.user,post[0],offset,limit)
	if not comments:
		temp['message']='no comments to be displayed'
		return temp
	commentserializer=CommentSerializer(comments,many=True)
	for i in range(len(commentserializer.data)):
		commentserializer.data[i]["description"]=HTMLParser.HTMLParser().unescape(strip_tags(commentserializer.data[i]["description"].strip()))
	temp['status']=1
	temp['message']='success'
	temp['data']=commentserializer.data
	return temp