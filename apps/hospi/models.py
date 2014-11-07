from django.db import models
from django.contrib.auth.models import User
from apps.users.models import UserProfile

class Hostel(models.Model):
    name = models.CharField(max_length=50,unique=True)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name=u'Type')

    def __unicode__(self):
        return (str(self.name) + ' (' + str(self.gender )+ ')')

    def get_room_count(self):
        return len(self.parent_hostel.all())

    def get_current_population(self):
        rooms = self.parent_hostel.all()
        population = 0
        for room in rooms:
            population += len(room.occupants.all())
        return population

class Room(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name / Number')
    hostel = models.ForeignKey(Hostel, related_name='parent_hostel')
    capacity = models.IntegerField(max_length=3)
    occupants = models.ManyToManyField(UserProfile, related_name='room_occupant', null=True, blank=True)

    def __unicode__(self):
        return (str(self.name) + ' (' + str(self.capacity) + ' max)')

    def get_occupants_count(self):
        return len(self.occupants.all())

class HospiTeam(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(UserProfile,related_name='hospi_team_leader')
    members = models.ManyToManyField(UserProfile,related_name='hospi_team_members', blank=True)
    team_sid = models.CharField(max_length=20)
    ACCOMODATION_CHOICES = (
        ('not_req', 'Accomodation not required'),
        ('requested', 'Accomodation requested'),
        ('confirmed', 'Request confirmed'),
        ('waitlisted', 'Waitlisted'),
        ('rejected', 'Rejected'),
        ('hospi', 'Added to hospi portal')
    )
    accomodation_status = models.CharField(max_length=50, choices=ACCOMODATION_CHOICES, default='not_req')
    city = models.CharField(max_length=100, null=True, blank=True)
    date_of_arrival = models.DateField(blank=True, null=True, default='2014-01-08')
    time_of_arrival = models.TimeField(blank=True,null=True, default='23:00:00')
    date_of_departure =  models.DateField(blank=True, null=True, default='2014-01-11')
    time_of_departure = models.TimeField(blank=True, null=True, default='10:00:00')
    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)
    mattress_count = models.IntegerField(default=0)
    mattress_returned = models.BooleanField(default=False)

    def __unicode__(self):
        try:
            ret_val = (str(self.name)+ ' lead by '+ str(self.leader))
        except Exception,e:
            ret_val = 'None'
        return ret_val

    def get_total_count(self):
        mem = len(self.members.all())
        return mem+1

    def get_male_count(self):
        M=['male', 'Male']
        mem = len(self.members.all().filter(gender='male'))
        if self.leader.gender in M:
            mem +=1
        return mem

    def get_female_count(self):
        F=['female', 'Female']
        mem = len(self.members.all().filter(gender='female'))
        if self.leader.gender in F:
            mem +=1
        return mem

    def is_mixed(self):
        if self.get_female_count() and self.get_male_count():
            return True
        else:
            return False

    def get_male_members(self):
        M=['male', 'Male']
        mem = list(self.members.filter(gender='male'))
        if self.leader.gender in M:
            mem.append(self.leader)
        return mem

    def get_female_members(self):
        F=['female', 'Female']
        mem = list(self.members.filter(gender='female'))
        if self.leader.gender in F:
            mem.append(self.leader)
        return mem

    def get_all_members(self):
        mem = list(self.members.all())
        mem.append(self.leader)
        return mem

class Allotment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(HospiTeam, related_name='alloted_team')
    alloted_by = models.ForeignKey(User, related_name='alloted_coord')

    def __unicode__(self):
        return self.team.name

class HospiLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='hospi_log_erp_user')
    user = models.ForeignKey(UserProfile, related_name='hospi_log_user')
    room = models.ForeignKey(Room, related_name='hospi_room')
    checked_out = models.BooleanField(default=False)
    checkout_time = models.DateTimeField(blank=True, null=True)
    checked_out_by = models.ForeignKey(User, related_name='hospi_check_out_erp_user',null=True, blank=True)
