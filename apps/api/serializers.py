from rest_framework import serializers

from apps.users.models import ERPProfile, UserProfile, Team
from apps.events.models import Event
from django.contrib.auth.models import User

from apps.walls.models import Wall, Post, Comment
from apps.blog.models import Category

class UserInfoSerializer(serializers.ModelSerializer):
    want_accomodation = serializers.BooleanField(source='profile.want_accomodation', required=False)
    mobile_number = serializers.CharField(source='profile.mobile_number', required=False)
    college_text = serializers.CharField(source='profile.college_text', required=False)
    class Meta:
        model = User
        # fields = ('id', 'first_name', 'last_name', 'email', 'password')
        exclude = ("password", "user_permissions", "username", "last_login", "is_staff", "is_superuser", "is_active", "groups", "date_joined")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
        # exclude = ("password", "user_permissions", "username", "last_login", "is_staff", "is_superuser", "is_active", "groups", "date_joined")

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ERPProfile

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event

class ParticipantProfileSerializer(serializers.ModelSerializer):
    email = serializers.BooleanField(source='user.email', required=False)    
    class Meta:
        model = UserProfile

class TeamSerializer(serializers.ModelSerializer):
    members = UserInfoSerializer(source='members', many=True)
    class Meta:
        model = Team

class WallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wall
        fields=('id','name','is_public','time_updated','cache_updated','person')
        depth=2
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','is_active','subject','by','description','time_created','time_updated','comments')
        depth = 2

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields=('id','is_active','access_specifier','description','by','time_created','time_updated','liked_users')
        depth = 1

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        depth = 2

#class NotificatioSerializer(serializers.Serializer):
#    id = serializers.IntegerField()
#    actor = serializers.CharField()
#    actor_id = serializers.IntegerField()
#    verb = serializers.CharField()
#    wall = serializers.CharField()
#    wall_id = serializers.IntegerField()
#    detail =
#
#
#    #json = []
#
#        #for notif in newsfeed:
#        #    item = {}
#        #    item['id'] = notif.id
#        #    item['actor'] = notif.actor.get_full_name()
#        #    item['actor_id'] = notif.actor.id
#        #    item['verb'] = notif.verb
#        #    item['wall'] = notif.target.wall.name
#        #    item['wall_id'] = notif.target.wall.id
#        #    item['description'] = notif.action_object.description
#        #    item['timestamp'] = notif.timestamp
#        #    json.append(item)
#
