"""
    A small file which just has all the imports which can be easily used for testing
    Useful in shell !

"""

# Django
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
# Apps
# Decorators
# Models
from misc.models import College
from apps.walls.models import Wall, Post
from apps.events.models import Event
# Forms
# View functions
# Misc
from misc.utils import *
from misc.constants import *
# Python
import datetime
