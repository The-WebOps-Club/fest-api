# Management related imports
from django.core.management.base import BaseCommand, CommandError, NoArgsCommand

# Models

from apps.blog.models import Category, Feed
# App imports
from configs import settings

# Python
import csv
import os
import datetime
import xlrd

class Command(BaseCommand):
	"""
		Add blogs from excel sheet
	"""
	help = 'Add blogs from excel sheets'

	def handle(self, arg1=None, **options):
	
		"""
			Arg1 = path of file to import blogs from
		"""
		if not arg1: 
			arg1 = "files/data/blogs.xls"
		arg_path = os.path.abspath(os.path.join(settings.PROJECT_PATH, arg1))
		self.stdout.write("Adding Blogs from the Database @ " + arg_path)
		try:	
			new_college_count = 0 
                        workbook = xlrd.open_workbook(arg_path)
                        worksheets = workbook.sheet_names()
                        for worksheet_name in worksheets:
                            worksheet = workbook.sheet_by_name(worksheet_name)
                            if len(Category.objects.filter(name = worksheet_name)) == 0:
                                category = Category.objects.create(name = worksheet_name)
                            else:
                                category = Category.objects.get(name=worksheet_name)
                            num_rows = worksheet.nrows - 1
                            num_cells = worksheet.ncols - 1
                            curr_row = -1
                            
                            while curr_row < num_rows:
                                curr_row += 1
                                row = worksheet.row(curr_row)
                                print 'Row:', curr_row
                                curr_cell = -1
                                title = worksheet.cell_value(curr_row, 0)
                                link = worksheet.cell_value(curr_row, 1)
                                if len(Feed.objects.filter(name=title, link=link)) == 0:
                                    new_feed = Feed.objects.create(name=title, link=link)
                                else:
                                    new_feed = Feed.objects.get(name=title, link=link)
                                new_feed.category.add(category)
                                new_feed.save
                                new_college_count += 1
                                print title, link

			self.stdout.write("Done line " + str(curr_row) + " of " + str(curr_row))
			self.stdout.write("Added " + str(new_college_count) + " colleges from " + str(curr_row) + " lines in file")
		except (OSError, IOError) as e:
			self.stdout.write("Was not able to open the file = " + str(arg_path) + "Check if it exists")
