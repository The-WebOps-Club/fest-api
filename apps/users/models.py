"""
    Handles all models related to users :
        - Dept : The department at the fest
        - SubDept : The sub-department at the fest
        - User Profile : Handles the basic information of people, their college, their fest related information
        - ERPProfile : Handles the information of a users organizational role

"""
# Django
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Q
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
# Apps
# Decorators
# Models
from misc.models import College
from apps.walls.models import Wall, Post
from misc.managers import CheckActiveManager

# Forms
# View functions
# Misc
from misc.utils import *
from misc.constants import *

from social.apps.django_app.default.models import UserSocialAuth
# Python
import datetime

# Department Models
class Dept(models.Model):
    """ 
        A model having data about specific Departments @ the fest 
    """
    is_active       = models.BooleanField(default=True)

    # Relations with other models
    wall            = models.OneToOneField(Wall, related_name='dept')
    
    # Basic information
    name            = models.CharField(max_length=30, unique=True)
    description     = models.TextField(max_length=500, null=True, blank=True)
    
    # Analytics
    time_updated    = models.DateTimeField(auto_now=True, default = datetime.datetime(1950, 1, 1))
    cache_updated   = models.DateTimeField(auto_now=True, default = datetime.datetime(1950, 1, 1))
    
    # Storage
    directory_id    = models.CharField( max_length = 100, null=True, blank=True )
    
    # Calendar
    calendar_id     = models.CharField( max_length = 100, null=True, blank=True )
    

    objects = CheckActiveManager()
    
    def __unicode__(self):
        return self.name

    def cores(self):
        return User.objects.filter(Q(erp_profile__core_relations__in=[self]) )
    def supercoords(self):
        return User.objects.filter(Q(erp_profile__supercoord_relations__in=[self]) )
    def coords(self):
        return User.objects.filter(Q(erp_profile__coord_relations__in=self.subdepts.all()) )
    def related_users(self):
        return User.objects.filter( \
            Q(erp_profile__core_relations__in=[self] ) | \
            Q(erp_profile__supercoord_relations__in=[self] ) | \
            Q(erp_profile__coord_relations__in=self.subdepts.all() )
        )

    def profile_pic(self):
        temp = settings.MEDIA_URL + "profile/dept/dp/" + self.id
        return temp
    
    def banner_pic(self):
        temp = settings.MEDIA_URL + "profile/dept/banner/" + self.id
        return temp
    
    

class Subdept(models.Model):
    """ 
        A model having data about specific SubDepartments @ the fest 
        Every subdept is linked to an event 
    """
    is_active       = models.BooleanField(default=True)

    # Relations with other models
    dept            = models.ForeignKey(Dept, related_name='subdepts')
    wall            = models.OneToOneField(Wall, related_name='subdept')
    # event           = models.ForeignKey(Event, null=True, blank=True)
    
    # Basic information
    name            = models.CharField(max_length=30, unique=True)
    description     = models.TextField(max_length=500, null=True, blank=True)

    # Analytics
    time_updated    = models.DateTimeField(auto_now=True, default = datetime.datetime(1950, 1, 1))
    cache_updated   = models.DateTimeField(auto_now=True, default = datetime.datetime(1950, 1, 1))

    # Storage
    directory_id    = models.CharField( max_length = 100, null=True, blank=True )
    

    objects = CheckActiveManager()

    def __unicode__(self):
        return self.name

    def cores(self):
        return [i.user for i in self.dept.core_set.all()]
    def supercoords(self):
        return [i.user for i in self.dept.supercoord_set.all()]
    def coords(self):
        return [i.user for i in self.coord_set.all()]
    def related_users(self):
        ret = set()
        ret.update( self.coords(), self.supercoords(), self.cores() )
        return list(ret)

    def profile_pic(self):
        temp = settings.MEDIA_URL + "profile/subdept/dp/" + self.id
        return temp
    def banner_pic(self):
        temp = settings.MEDIA_URL + "profile/subdept/banner/" + self.id
        return temp

class Page(models.Model):
    """ 
        A model having data about a page. An equivalent of a group
    """
    is_active       = models.BooleanField(default=True)

    # Relations with other models
    wall            = models.OneToOneField(Wall, related_name='page')
    
    # Basic information
    name            = models.CharField(max_length=30, unique=True)
    description     = models.TextField(max_length=500, null=True, blank=True)

    # Analytics
    time_updated    = models.DateTimeField(auto_now=True, default = datetime.datetime(1950, 1, 1))
    cache_updated   = models.DateTimeField(auto_now=True, default = datetime.datetime(1950, 1, 1))

    # Storage
    directory_id    = models.CharField( max_length = 100, null=True, blank=True )

    # Calendar
    calendar_id     = models.CharField( max_length = 100, null=True, blank=True )
    
    objects = CheckActiveManager()

    def __unicode__(self):
        return self.name

    def related_users(self):
        return self.user_set.all()

    def profile_pic(self):
        temp = settings.MEDIA_URL + "profile/page/dp/" + self.id
        return temp
    def banner_pic(self):
        temp = settings.MEDIA_URL + "profile/page/banner/" + self.id
        return temp

class UserProfile(models.Model): # The corresponding auth user
    """
        The model is a basic model for any user who will come into Fest.
        
        It handles the basic 
    
    """
    is_active       = models.BooleanField(default=True)

    user               = models.OneToOneField(User, related_name='profile') # uses name and email from here. username = email
    
    # Basic information
    gender             = models.CharField(max_length=1, choices=GENDER_CHOICES, default='F')
    dob                = models.DateField(null=True, blank=True, help_text='Date format should be dd-mm-yyyy')
    mobile_number      = models.CharField(max_length=15, blank=True, null=True, help_text='Please enter your current mobile number')
    
    # College info
    branch             = models.CharField(max_length=50, choices=BRANCH_CHOICES, help_text='Your branch of study')
    college            = models.ForeignKey(College, null=True, blank=True)
    college_roll       = models.CharField(max_length=40, null=True)
    school_student     = models.BooleanField(default=False)
    
    # Fest related info
    want_accomodation  = models.BooleanField(default=False, help_text = "Doesn't assure accommodation.")
    
    # Internal flags and keys
    activation_key     = models.CharField(max_length=40, null=True)
    key_expires        = models.DateTimeField(default=timezone.now() + datetime.timedelta(2))
    
    # Fest organizational info
    # is_core            = models.BooleanField(default=False)
    # is_hospi           = models.BooleanField(default=False)
  


  #Events registerd

#events_registered  = models.ManyToManyField(Event, null=True, blank=True, related_name='participant')
    # Analytics information
    date_created       = models.DateTimeField(auto_now_add=True)
    last_activity_ip   = models.IPAddressField(default="0.0.0.0")
    last_activity_date = models.DateTimeField(default = datetime.datetime(1950, 1, 1))

    send_mails         = models.BooleanField(default=True)
    
    objects = CheckActiveManager()

    @property
    def fest_id(self):
        return settings.FEST_NAME[:2].upper + str(self.user.id).zfill(6)
        
    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                         seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    def save(self, *args, **kwargs):
        #self.user.save()
        super(UserProfile, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.user.delete()
        super(UserProfile, self).delete(*args, **kwargs)
    
    def set_iitm_user(self, *args, **kwagrs):
        try:
            self.college = College.objects.get(name__iexact="IIT MADRAS", state__iexact="Tamil Nadu")
            self.save()
        except:
            pass

    def get_absolute_url(self):
        return reverse('apps.users.views.profile', args=(self.user.pk,))

    def get_pic(self, s=75):
        url = "graph.facebook.com" + self.fbid + "/picture"
        return url

    @property
    def fbid(self):
    	fb_accts = UserSocialAuth.objects.filter(provider="facebook", user=self.user)
        if len(fb_accts):
            return fb_accts[0].uid
        return ""
        
    def incomplete(self):
        self_user = self.user
        return self_user.get_full_name() and self.mobile_number and \
            self_user.email

    def create_unsubscribe_link(self):
        username, token = self.make_token().split(":", 1)
        return reverse('apps.users.views.unsubscribe', kwargs={'username': username, 'token': token,})
 
    def make_token(self):
        return TimestampSigner().sign(self.user.username)
 
    def check_token(self, token):
        try:
            key = '%s:%s' % (self.user.username, token)
            TimestampSigner().unsign(key, max_age=60 * 60 * 48) # Valid for 2 days
        except BadSignature, SignatureExpired:
            return False
        return True

    def __unicode__(self):
        return self.user.first_name
    
    class Admin:
        pass

class ERPProfile(models.Model):
    # Relations to other models
    is_active       = models.BooleanField(default=True)

    user            = models.OneToOneField(User, related_name='erp_profile') # uses name and email from here. username = email
    wall            = models.OneToOneField(Wall, related_name='person')
    
    # Temporary role in the Fest after selecting which identity he is
    # dept            = models.ForeignKey(Dept, related_name='dept_user_set')
    # subdept         = models.ForeignKey(Subdept, blank=True, null=True, default=None, related_name='subdept_user_set')
    # level           = models.IntegerField(default=0) # 0 = Coord, 1 = Supercoord, 2 = Core
    
    # Shaastra Relations - all possible roles in the fest
    coord_relations = models.ManyToManyField(Subdept, null=True, blank=True, related_name='coord_set')
    supercoord_relations = models.ManyToManyField(Dept, null=True, blank=True, related_name='supercoord_set')
    core_relations  = models.ManyToManyField(Dept, null=True, blank=True, related_name='core_set')
    page_relations  = models.ManyToManyField(Page, null=True, blank=True, related_name='user_set')
    
    # Other random information for profile
    nickname        = models.CharField(max_length=100, blank=True, null=True)
    room_no         = models.IntegerField(default=0, blank=True, null=True )
    hostel          = models.CharField(max_length=15, choices = HOSTEL_CHOICES, blank=True, null=True)
    summer_number   = models.CharField(max_length=10, blank=True, null=True)
    
    # Holiday stay
    summer_stay     = models.CharField(max_length=100, blank=True, null=True)
    winter_stay     = models.CharField(max_length=100, blank=True, null=True)
    summer_stay2    = models.CharField(max_length=100, blank=True, null=True)
    winter_stay2    = models.CharField(max_length=100, blank=True, null=True)

    objects = CheckActiveManager()

    @property
    def name(self):
        return self.user.get_full_name()

    def get_name(self):
        if self.nickname:
            return self.nickname
        else:
            return self.user.get_full_name()
        
    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)
        # return self.user.last_login

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                         seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False
    
    def __unicode__(self):
        return self.get_name()

    def incomplete(self):
        return self.user.get_full_name() and self.user.email and \
            self_user.email

    def related_walls(self):
        from apps.walls.utils import get_my_walls
        return get_my_walls(self)

    # Methods to check for position/role
    def is_coord(self, request):
        return request.session["role"] == "coord"
    def is_supercoord(self, request):
        return request.session["role"] == "supercoord"
    def is_core(self, request):
        return request.session["role"] == "core"
    def get_position (self, request):
        return request.session["role"].title()
    
    def relations_count(self):
        return self.core_relations.count() + self.supercoord_relations.count() + self.coord_relations.count()

    def save(self, *args, **kwargs):
        if not hasattr(self.user, "profile"):
            user_profile = UserProfile(user=self.user)
            user_profile.set_iitm_user() # As every user with ERPProfile is in iit
            user_profile.save()
        temp = super(ERPProfile, self).save(*args, **kwargs)
        return 

    def get_absolute_url(self):
        return reverse('apps.users.views.profile', args=(self.user.pk,))
