fest-api
========

An API implementation for Saarang Shaastra like fests, including ERP and Mainsite and Mobile interface

1. Setup :
	- Create a virtual env
		- install `python-virtualenv`
		- Go into the folder of the git repository and use `virtualenv --no-site-packages venv`
	- Install configs/requirements.txt
		- use 
			```
			pip install -r config/requirements.txt
			```
		- and then to make sure of all versions
			```
			pip install -r config/requirements.txt --upgrade
			```
	- Install `libmysqlclient-dev python-dev` if not already installed
	- Modify configs/settings.sample.py to configs/settings.py with appropriate modifications


2. TastyPie :
    - Till now, tastypie(v1.11) has some issues with through tables.
    - Need to replace (in the save_m2m function ~line 2300): 
     
    	```
     	related_mngr.add(*related_objs)
     	```
      with :
      	```
      	if hasattr(related_mngr, 'add'):
			related_mngr.add(*related_objs)
		else:
			# handle m2m with a "through" class
			for other_obj in related_objs:
				related_mngr.through.objects.get_or_create(**{
					related_mngr.source_field_name: bundle.obj,
					related_mngr.target_field_name: other_obj
				})
		```

3. Setup Social Accounts :
	. FACEBOOK
		- Add your facebook credentials (token, key) into settings

	. GOOGLE
		- Go to `{{SITE_URL}}/docs/refresh_token` to create a new refresh token.
		- This will ask access to a Google account - use the account on which to store Docs and accept.
		- Now this will store the refresh_token in a configs file and ask you to restrat server.
		- Restart Server to refetch all settings.
		- Now you can access Google Drive and Google Picker API
		
		- Also, add google credentials into settings
			- Gogole Public Key
			- Google oauth configs into configs/docs_oauth2_credentials.json
		
	. GITHUB
		- Add your github credentials (token, key) into settings
    

4. Setup Database Appropriately :
	. Management command `basic_setup` is used to populate some data - Colleges from Shaastra 2014 (optional)
	. Management command `update_email_templates` is used to update email templates and store onto the database for Django Post office (optional)
	. Management command `populate_db` can be used to get dummy data
	. Management command `jsonify_data` is used by atwho for data. Autogenerates some json objects which are easy to use
	
	. 