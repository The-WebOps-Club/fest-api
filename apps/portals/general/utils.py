# utils.py
from django.conf import settings
from apps.users.models import Subdept, Dept, Page
from django.contrib.auth.models import User

def attach_drive_to_entity( drive, entity ):
	title = entity.name
	description = title +'\'s Drive Folder'
	mime_type = 'application/vnd.google-apps.folder'
	if( isinstance(entity, Subdept) ):
		parent_id = entity.dept.directory_id
		if parent_id is None :
			raise ValueError('Subdept\'s Dept does not have a folder. Attach drive to dept first')
	else:
		parent_id = settings.GOOGLE_DRIVE_ROOT_FOLDER_ID

	if parent_id is None :
		raise ValueError('parent_id not set')

	folder = drive.insert_file( title, description, parent_id, mime_type, title, folder = True )
	entity.directory_id = folder["id"]
	entity.save()

def share_drive( drive, entity, directory_id = None ):
	if( isinstance(entity, User) ):
		if directory_id is None :
			raise ValueError('Directory ID missing.')
		drive.set_permission(directory_id, value=entity.email, perm_type='user', role='writer')
		return

	directory_id = entity.directory_id
	if directory_id is None :
		raise ValueError('Entity does not have a drive reference. Attach drive to entity first.')

	profile_set = [];
	if( isinstance(entity, Subdept) ):
		profile_set += list(entity.coord_set.all())
	elif( isinstance(entity, Dept) ):
		profile_set += list(entity.core_set.all()) + list(entity.supercoord_set.all())
	elif( isinstance(entity, Page) ):
		profile_set += list(entity.user_set.all())

	for profile in profile_set :
		user = profile.user
		share_drive( drive, user, directory_id )
		
def attach_calendar_to_entity( calendar, entity ):
	title = entity.name
	description = title +'\'s Calendar'
	
	calendar_details = {
	    'summary': description,
	    'timeZone': 'Asia/Kolkata'
	}

	created_calendar = calendar.service.calendars().insert(body=calendar_details).execute()

	print created_calendar['id']
	
	entity.calendar_id = created_calendar['id']
	entity.save()

def share_calendar( calendar, entity, calendar_id = None ):
	if( isinstance(entity, User) ):
		if calendar_id is None :
			raise ValueError('Calendar ID missing.')
		
		rule = {
		    'scope': {
			'type': 'user',
			'value': entity.email,
		    },
		    'role': 'owner'
		}
		print calendar_id.split('@')[0]
		created_rule = calendar.service.acl().insert(calendarId=calendar_id, body=rule).execute()
		print entity.email
		print calendar_id
		print created_rule['id']
		print "================================"
		return

	calendar_id = entity.calendar_id
	if calendar_id is None :
		raise ValueError('Entity does not have a calendar reference. Attach calendar to entity first.')

	profile_set = [];
	if( isinstance(entity, Dept) ):
		profile_set += list(entity.related_users())#User
	elif( isinstance(entity, Page) ):
		profile_set += [x.user for x in list(entity.user_set.all())]#ERPProfile
	print list(set(profile_set))
	for user in list(set(profile_set)) :
		share_calendar( calendar, user, calendar_id )