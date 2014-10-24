from rest_framework import serializers

from apps.users.models import ERPProfile, UserProfile, Team
from apps.events.models import Event
from django.contrib.auth.models import User

from apps.walls.models import Wall, Post, Comment
from apps.blog.models import Category
from apps.events.models import EventRegistration
from apps.spons.models import SponsImageUpload
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name', 'email', 'password')

class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = ERPProfile

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('eventtab_set','name', 'short_description', 'event_type', 'category', 'has_tdp', 'team_size_min', 'team_size_max', 'registration_starts', 'registration_ends', 'google_group', 'email', 'users_registered', 'teams_registered', 'coords', 'is_visible')
	model = Event
        depth = 1

class ParticipantProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfile

class TeamSerializer(serializers.ModelSerializer):
	members = UserSerializer(source='members', many=True)
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
        fields = ('id','name', 'feeds')
        depth = 1
        depth = 2
class EventRegistrationSerializer(serializers.ModelSerializer):
	class Meta:
		model=EventRegistration
		depth=1

class EventDisplaySerializer(serializers.ModelSerializer):
    class Meta:
		model = Event
		depth=1
		fields=("id","name","short_description","event_type", "category","has_tdp","team_size_min","team_size_max","registration_starts","registration_ends","google_group","email","long_description","google_form","event_image","is_visible",'eventtab_set',)
		
class SponsImageUploadSerializer(serializers.ModelSerializer):
	class Meta:
		model= SponsImageUpload
class UserProfileEditSerializer(serializers.ModelSerializer):
	class Meta:
		model = ERPProfile
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
