from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from apps.users.models import UserProfile
from django.conf import settings
from django.core.exceptions import ValidationError
import datetime
import os
import xlrd
"""
# Barcode Excel Sheet
# Assumes a 2 column, n row excel sheet.
# If data starts from line n, set curr_row to (n-1)
def link_barcode_excel():
    workbook = xlrd.open_workbook('path/xxx.xls')
    worksheet = workbook.sheet_by_index(0)
    num_rows = worksheet.nrows - 1
    curr_row = -1
    while curr_row < num_rows:
        curr_row += 1
        row = worksheet.row(curr_row)
        #curr_cell = -1
        #while curr_cell < num_cells:
        #    curr_cell += 1
        #     #Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
        #    cell_type = worksheet.cell_type(curr_row, curr_cell)
        #    cell_value = worksheet.cell_value(curr_row, curr_cell)
        u = get_object_or_None(UserProfile,user__username=str(worksheet.cell_value(curr_row,0))
        if u:
            u.barcode = str(worksheet.cell_value(curr_row, 1))
            u.save()
"""
class Command(BaseCommand):
    help = 'Links the barcode number to the shaastra/saarang id, input taken from excel sheet'

    def handle(self, arg, **options):
        workbook = xlrd.open_workbook(arg)               #path of the workbook goes here
        worksheets = workbook.sheet_names()
        for worksheet_name in worksheets:
            worksheet = workbook.sheet_by_name(worksheet_name)
            num_rows = worksheet.nrows - 1
            curr_row = -1
            while curr_row < num_rows:
                curr_row += 1
                row = worksheet.row(curr_row)
                #curr_cell = -1
                #while curr_cell < num_cells:
                #    curr_cell += 1
                #     #Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                #    cell_type = worksheet.cell_type(curr_row, curr_cell)
                #    cell_value = worksheet.cell_value(curr_row, curr_cell)
                u = get_object_or_None(UserProfile,user__username=str(worksheet.cell_value(curr_row,0)))
                if u is not None:
                    u.barcode = str(worksheet.cell_value(curr_row, 1))
                    u.save()

