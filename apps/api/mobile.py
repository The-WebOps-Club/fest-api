import HTMLParser
import urllib
import os
import glob
from django.utils.html import strip_tags
from django.conf import settings
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from apps.walls.models import Post
from apps.walls.utils import query_notifs, query_newsfeed,get_my_walls,get_my_posts,get_comments
from apps.walls.models import Wall,Post
from apps.api.serializers import *
from apps.walls.ajax import create_post,create_comment
from apps.api.utils import *
from apps.users.models import UserProfile, Team
from apps.blog.models import Category, Feed

from annoying.functions import get_object_or_None
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.csrf import csrf_exempt

USER_MUTABLE_FIELDS = ["password", "first_name", "last_name"];
PROFILE_MUTABLE_FIELDS = ["college_roll","gender","dob","mobile_number","branch","college","college_text","school_student","want_accomodation","age","city"];
EVENT_MUTABLE_FIELDS = ["has_tdp","team_size_min","team_size_max","registration_starts","registration_ends"];

class NotificationViewSet(viewsets.ViewSet):
    """
        Return Notifications to an authenticated User
        page -- Start page number
        limit -- number of items in each page
        type --  type of notification to get
    """
    def list(self, request):
        page = int(request.QUERY_PARAMS.get('page', 0))
        limit = int(request.QUERY_PARAMS.get('limit', 10))
        notif_type = request.QUERY_PARAMS.get('type', 'all')
        message = ''
        data = []
        json = []
        if notif_type == 'all':
            notifs = query_newsfeed(request.user, page=page, max_items=limit)
        else:
            notifs = query_notifs(request.user, page=page, max_items=limit, notif_type=notif_type)
        if not notifs:
            message='no notifications to be displayed'
            return Response(viewset_response(message,data))
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
            target_type = "post"
            target_name = notif.target.subject
            target_id = notif.target.id
            item['target'] = {}
            item['target']['type'] = target_type
            item['target']['name'] = target_name
            item['target']['id'] = target_id
            item['description'] = HTMLParser.HTMLParser().unescape(strip_tags(notif.action_object.description.strip()))
            item['timestamp'] = notif.timestamp
            json.append(item)
        data=json
        return Response(viewset_response(message,data))

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
    """
    Return walls of an user
    """

    def list(self,request):
        message = ''
        data = []
        walls = get_my_walls(request.user)
        if not walls :
            message='no walls to be displayed'
            return Response(viewset_response(message,data))
        wallserializer=WallSerializer(walls,many=True)
        data=wallserializer.data
        return Response(viewset_response(message,data))

class PostsViewSet(viewsets.ViewSet):
    def list(self,request):
        """
        Return posts to an authenticated User
        limit -- number of items to be returned
        offset -- offset
        wall_id --  wall id or post id
        """
        message=''
        data=[]
        wall_id=request.QUERY_PARAMS.get('wall_id')
        offset=request.QUERY_PARAMS.get('offset')
        limit=request.QUERY_PARAMS.get('limit')

        if not wall_id:
            message='please enter wall id'
            return Response(viewset_response(message,data))
        wall= Wall.objects.filter(id=int(wall_id))
        if not wall:
            message='no wall with that id exists'
            return Response(viewset_response(message,data))
        posts = get_my_posts(request.user,wall,offset,limit)
        try:
            if posts['error']:
                message=posts['error']
                return Response(viewset_response(message,data))
        except:
            pass
        if not posts:
            message='no post with that id exists'
            return Response(viewset_response(message,data))
        postserializer = PostSerializer(posts,many=True)
        for i in range(len(postserializer.data)):
            postserializer.data[i]["description"]=HTMLParser.HTMLParser().unescape(strip_tags(postserializer.data[i]["description"].strip()))
            for j in range(len(postserializer.data[i]["comments"])):
                postserializer.data[i]["comments"][j]["description"] = HTMLParser.HTMLParser().unescape(strip_tags(postserializer.data[i]["comments"][j]["description"].strip()))
        data=postserializer.data
        return Response(viewset_response(message,data))


    def create(self,request):
        wall_id=request.QUERY_PARAMS.get('wall_id')
        post=request.POST
        message=''
        data=[]
        new_post_subject=str(request.POST['new_post_subject'])
        if not new_post_subject:
            message='please enter text to post'
            return Response(viewset_response(message,data))
        data.append(new_post_subject)
        post=urllib.urlencode(post,True)
        created=create_post(request,wall_id,post)
        if created:
            return Response(viewset_response(message,data))
        else:
            message='an error has occured while trying to comment'
            return Response(message,data)
    #def delete(self,request):
    #   pass

class CommentsViewSet(viewsets.ViewSet):
    def list(self,request):
        post_id=request.QUERY_PARAMS.get('post_id')
        offset=request.QUERY_PARAMS.get('offset')
        limit=request.QUERY_PARAMS.get('limit')
        data=[]
        message=''
        if not post_id:
           message='please enter post id'
           return Response(viewset_response(message,data))
        try:
            post=Post.objects.get(id=int(post_id))
        except Post.DoesNotExist:
        # TODO : add check_access rights or post
            message='no post with that id exists'
            return Response(viewset_response(message,data))
        postserializer=PostSerializer(post)
        postserializer.data["description"]=HTMLParser.HTMLParser().unescape(strip_tags(postserializer.data["description"].strip()))
        for j in range(len(postserializer.data["comments"])):
            postserializer.data["comments"][j]["description"] = HTMLParser.HTMLParser().unescape(strip_tags(postserializer.data["comments"][j]["description"].strip()))
        data=postserializer.data
        return Response(viewset_response(message,data))

        #if not comments:
        #   message='no comments to be displayed'
        #   return Response(viewset_response(message,data))
        #commentserializer=CommentSerializer(comments,many=True)

        #for i in range(len(commentserializer.data)):
        #   commentserializer.data[i]["description"]=HTMLParser.HTMLParser().unescape(strip_tags(commentserializer.data[i]["description"].strip()))
        #data=commentserializer.data
        #return Response(viewset_response(message,data))

    def create(self,request):
        post_id=request.QUERY_PARAMS.get('post_id')
        message=''
        data=[]
        created=0
        comment=request.POST
        comment_text=str(request.POST['comment'])
        if not comment_text:
            message='please enter text to comment'
            return Response(viewset_response(message,data))
        data.append(comment_text)
        comment=urllib.urlencode(comment,True)
        created=create_comment(request, post_id, comment)
        if created:
            return Response(viewset_response(message,data))
        else:
            message='an error has occured while trying to comment'
            return Response(message,data)

class UserProfileViewSet(viewsets.ViewSet):
    def list(self, request):
        user = self.request.user
        data = ParticipantProfileSerializer(UserProfile.objects.get_or_create( user = self.request.user )[0]).data
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['user_id'] = user.id
        return Response(viewset_response("done", data))

    def create(self, request):
        user = self.request.user
        profile = UserProfile.objects.get_or_create( user=user )[0]
        try:
            for i in request.DATA:
                if i == "college": # foreign key
                    pass
                elif i in PROFILE_MUTABLE_FIELDS and i != '':
                    setattr( profile, i, request.POST[i] )
                elif i in USER_MUTABLE_FIELDS and i != '':
                    setattr( user, i, request.POST[i] )
        except:
            return Response({
                "message": "Invalid input data."
            }, status=status.HTTP_400_BAD_REQUEST);
        profile.save()
        user.save()
        data = ParticipantProfileSerializer(profile).data
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        return Response( viewset_response( "done", data ) )

class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(viewset_response("done", UserSerializer(self.request.user).data))

    def create(self, request):
        user = self.request.user
        try:
            for i in request.POST:
                if i in USER_MUTABLE_FIELDS:
                    setattr( user, i, request.POST[i] )
        except:
            return Response("Invalid input data.",[]);
        user.save()
        return Response( viewset_response( "done", UserSerializer(user).data ) )

class TeamViewSet(viewsets.ViewSet):
    def  list(self, request):
        user = self.request.user
        teams = TeamSerializer(user.teams.all())
        teams_data = teams.data
        return Response(viewset_response("done", teams_data))

    def create(self, request):
        user = self.request.user
        action = request.DATA.get('action', 'edit')
        if action == "delete":
            # Delete the team
            if 'id' in request.DATA:
                team = Team.objects.get(id=request.DATA['id'])
                team.delete()
                return Response({
                    "success": "Successfully deleted"
                }, status=status.HTTP_202_ACCEPTED)
            else: # Create a new Team
                return Response({
                    "id": "Please select a team to delete"
                }, status=status.HTTP_400_BAD_REQUEST)
        elif action == "edit":

            member_list = set()
            member_list.add(user)
            if 'id' in request.DATA:
                team = Team.objects.get(id=request.DATA['id'])
            else: # Create a new Team
                team = Team()
                if Team.objects.filter(name=request.DATA['name']):
                    return Response({
                        "name": "This team name is already used"
                    }, status=status.HTTP_400_BAD_REQUEST)
                if request.DATA['name'] == "":
                    return Response({
                        "name": "The team name is required"
                    }, status=status.HTTP_400_BAD_REQUEST)

            team.name = request.DATA['name']
            member_list_data = request.DATA.getlist('member[]', [])

            if len(member_list_data) == 0 :
                return Response({
                    "member": "You need atleast 1 member in a team !"
                }, status=status.HTTP_400_BAD_REQUEST)
            for i in member_list_data:
                try:
                    i = int(i)
                except ValueError:
                    i = -1 # Didnt wanna type the error message again -_-
                try:
                    member_list.add(User.objects.get(id=i))
                except User.DoesNotExist:
                    return Response({
                        "member": "The members you have given seem to be invalid. Check the Shaastra IDs again"
                    }, status=status.HTTP_400_BAD_REQUEST)
            member_list = list(member_list)

            team.save()
            team.members.clear() # Clear and add all members again
            team.members.add(*member_list)

            data = TeamSerializer(team).data
            return Response( viewset_response( "done", data ) )
        else:
            return Response({
                "error": "An error occured ! Please contact webops team at : <a href='mailto:webops@shaastra.org'>webops@shaastra.org</a>"
            }, status=status.HTTP_400_BAD_REQUEST)

# API methods for Blog App
class BlogFeedViewSet(viewsets.ModelViewSet):
    """
        API for acessing blog feeds
    """
    queryset = Category.objects.all()
    serializer_class = BlogSerializer

class EventViewSet(viewsets.ViewSet):
    def list(self, request):
        user = self.request.user
        action_for = request.GET.get('action_for', 'all')
        action_for_id = request.GET.get('action_for_id', '')

        if action_for == "all": # Find all events.
            events_list = Event.objects.all()
            events_list = EventSerializer(events_list)
            events_data = events_list.data
        elif action_for == "user": # Find all events of mine
            events_list = EventSerializer(user.events_registered.all())
            events_data = events_list.data
        elif action_for == "team": # Find all events in my team
            team = get_object_or_None(Team, id=action_for_id)
            if team and team in user.teams.all():
                events_list = EventSerializer(team.events_registered.all())
                events_data = events_list.data
            else :
                return Response({
                    "error": "Cannot find this team in your list of teams !"
                }, status=status.HTTP_400_BAD_REQUEST)
        elif action_for == "id": # Find all events with id
            event = Event.objects.filter(id=action_for_id)
            if event:
                events_list = EventSerializer(event)
                events_data = events_list.data
            else :
                return Response({
                    "error": "Cannot find this event !"
                }, status=status.HTTP_400_BAD_REQUEST)
        elif action_for == "name": # Find all events with name
            event = Event.objects.filter(name=action_for_id)
            if event:
                events_list = EventSerializer(event)
                events_data = events_list.data
            else :
                return Response({
                    "error": "Cannot find this event !"
                }, status=status.HTTP_400_BAD_REQUEST)

        for ev in events_data:
            ev['is_mine'] = False
            # Handle whether the user is registered for the event
            if user.id in ev['users_registered']:
                ev['is_mine'] = True
                fname = settings.MEDIA_ROOT + "tdp/" + ev['name']+"/" + str(user.id) + ".*"
                url = glob.glob(fname)
                if len(url) >= 1:
                    url = url[0].replace(settings.MEDIA_ROOT, settings.MEDIA_URL) # Remove patha nd add url
                else:
                    url = ""
                ev['tdp_submitted'] = url
            else:
                user_team_ids = user.teams.values_list('id', flat=True) # get a list of all team ids
                for team in ev['teams_registered']:

                    if team in user_team_ids:
                        ev['is_mine'] = True
                        fname = settings.MEDIA_URL + "tdp/" + ev['name']+"/" + str(team) + ".*"
                        url = glob.glob(fname)
                        if len(url) >= 1:
                            url = url[0].replace(settings.MEDIA_ROOT, settings.MEDIA_URL) # Remove patha nd add url
                        else:
                            url = ""
                        ev['tdp_submitted'] = url
        return Response(viewset_response("done", events_data))

    def create(self, request):
        user = self.request.user
        event_id = request.POST.get('event_id', None)
        name = request.POST.get('name', None)
        action = request.POST.get('action', 'register')
        event = None

        if event_id:
            event = get_object_or_None(Event, id=event_id)
        elif name:
            event = get_object_or_None(Event, name=name)

        if not event:
            return Response({
                "error": "Cannot find this event ! Please contact webops team at : <a href='mailto:webops@shaastra.org'>webops@shaastra.org</a>"
            }, status=status.HTTP_400_BAD_REQUEST)

        if action == "register":
            if event.is_team_event:
                # Take team info
                team_name = request.DATA.get('team', None)
                if not team_name :
                    return Response({
                        "error": "You need to enter a team name."
                    }, status=status.HTTP_400_BAD_REQUEST)
                team = get_object_or_None(Team, name=team_name)
                if not team:
                    return Response({
                        "error": "There exists no such team. You need to create the team first !"
                    }, status=status.HTTP_400_BAD_REQUEST)
                if not team in user.teams.all():
                    return Response({
                        "error": "You are not a member of this team ! Ask the members to add you first."
                    }, status=status.HTTP_400_BAD_REQUEST)

                event.teams_registered.add(team)
                # ALSO TAKE FILE
                if request.FILES.get('tdp', None) and event.has_tdp:
                    f = request.FILES.get('tdp')
                    fileName, fileExtension = os.path.splitext(f.name)
                    fname = os.path.join(settings.MEDIA_ROOT, "tdp", event.name, str(team.id) + fileExtension)
                    handle_uploaded_file(f, fname)
                data = EventSerializer(event).data
                return Response( viewset_response( "done", data ) )
            else:
                # Take participant info
                event.users_registered.add(user)
                # ALSO TAKE FILE
                if request.FILES.get('tdp', None) and event.has_tdp:
                    f = request.FILES.get('tdp')
                    fileName, fileExtension = os.path.splitext(f.name)
                    fname = os.path.join(settings.MEDIA_ROOT, "tdp", event.name, str(user.id) + fileExtension)
                    handle_uploaded_file(f, fname)
                data = EventSerializer(event).data
                return Response( viewset_response( "done", data ) )
        elif action == "edit":

            try:
                for i in request.POST:
                    if i in EVENT_MUTABLE_FIELDS:
                        setattr( event, i, request.POST[i] )
            except:
                return Response("Invalid input data.",[]);
            event.save()
            return Response( viewset_response( "done", EventSerializer(event).data ) )
        elif action == "unregister":
            if event.is_team_event:
                team_name = request.DATA.get('team', None)
                if not team_name :
                    return Response({
                        "error": "You need to enter a team name."
                    }, status=status.HTTP_400_BAD_REQUEST)
                team = get_object_or_None(Team, name=team_name)
                if not team :
                    return Response({
                        "error": "There exists no such team. You need to create the team first !"
                    }, status=status.HTTP_400_BAD_REQUEST)
                if not team in user.teams.all():
                    return Response({
                        "error": "You are not a member of this team ! Ask the members to add you first."
                    }, status=status.HTTP_400_BAD_REQUEST)
                event.teams_registered.remove(team)
                if event.has_tdp:
                    fname = settings.MEDIA_ROOT + "tdp/" + event.name + "/" + str(team.id) + ".*"
                    fname = glob.glob(fname)[0]
                    try:
                        os.remove(fname)
                    except OSError:
                        pass

                data = EventSerializer(event).data
                return Response( viewset_response( "done", data ) )
            else:
                event.users_registered.remove(user)
                if event.has_tdp:
                    fname = settings.MEDIA_ROOT + "tdp/" + event.name + "/" + str(user.id) + ".*"
                    fname = glob.glob(fname)[0]
                    try:
                        os.remove(fname)
                    except OSError:
                        pass
                data = EventSerializer(event).data
                return Response( viewset_response( "done", data ) )
        else:
            return Response({
                "error": "An error occured ! Please contact webops team at : <a href='mailto:webops@shaastra.org'>webops@shaastra.org</a>"
            }, status=status.HTTP_400_BAD_REQUEST)
