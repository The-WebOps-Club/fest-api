# Management related imports
from django.core.management.base import BaseCommand, CommandError, NoArgsCommand

# Models
from django.contrib.auth.models import User
from apps.users.models import Dept, Subdept, ERPProfile
from apps.walls.models import Wall, Post, Comment
from misc.models import College

# App imports
from configs import settings

# Python
import csv
import os
import datetime

class Command(BaseCommand):
	"""
		Give all users access rights to everyone
	"""
	help = 'Does some simple pre configurations'

	def handle(self, arg1=None, **options):
	
		"""
			Arg1 = path of file to import colleges from
		"""
		if not arg1: 
			arg1 = "files/data/colleges_2014.csv"
		arg_path = os.path.abspath(os.path.join(settings.PROJECT_PATH, arg1))
		self.stdout.write("Adding Colleges from the Database @ " + arg_path)
		try:	
			new_college_count = 0
			with open(arg_path, 'rb') as csvfile:
				csvreader = csv.reader(csvfile)
				max_lines = len(list(csvreader))
			with open(arg_path, 'rb') as csvfile:
				csvreader = csv.reader(csvfile)
				for i, row in enumerate(csvreader):
					data = [k.strip() for k in row[1:]]
					if College.objects.filter(name=data[0], city=data[1], state=data[2]).count() == 0:
						College.objects.create(name=data[0], city=data[1], state=data[2])
						new_college_count += 1
					if (i % 50) == 0:
						self.stdout.write("Done line " + str(i) + " of " + str(max_lines))
			self.stdout.write("Added " + str(new_college_count) + " colleges from " + str(max_lines) + " lines in file")
		except (OSError, IOError) as e:
			self.stdout.write("Was not able to open the file = " + str(arg_path) + "Check if it exists")
