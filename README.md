fest-api
========

An API implementation for Saarang Shaastra like fests, including ERP and Mainsite and Mobile interface

1. Setup :
	- Create a virtual env
		- install `python-virtualenv`
		- Go into the folder of the git repository and use `virtualenv --no-site-packages venv`
		- ##If you do not know what git repository means read 'http://rogerdudler.github.io/git-guide/' for a begginer crash course
		- ##If you do not know what python-virtualenv means read 'http://www.pythonforbeginners.com/basics/python-virtualenv-usage'   
	- Install configs/requirements.txt
		- - Install `libmysqlclient-dev python-dev` using 'apt-get install libmysqlclient-dev python-dev'
		- use 
			```
			pip install -r configs/requirements.txt (read 8.c if pip is not installed. 
			```
		- and then to make sure of all versions
			```
			pip install -r configs/requirements.txt --upgrade
			```
	- Install `libmysqlclient-dev python-dev` if not already installed
	- (If a previous version of django is already installed or if you are not sure if you have a previous version read 8.d)

2. Change the following in the fest-api/configs/sample.setting.py

	- Change the filename to setings.py
	- Set the database settings (If you need details on how to do this read 8.a. If you are having problems with mysql installation follow 8.b)
	- (specific to ERP) In globalsettings.py set  'USE_EXTERNAL_SITES' to False 
	- In terminal type 'python manage.py syncdb' followed by 'python manage.py migrate'. If these 2 worked your database settings worked fine


4. Tastypie (NOT NEEDED for ERP)
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

4.  Setup Social Accounts : (NOT NEEDED for ERP)

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
    

5. Setup Database Appropriately :
 
	. Management command `add_colleges` is used to populate some data - Colleges from Shaastra 2014 (optional) (In other words type 'python manage.py add_colleges')

	. Management command `update_email_templates` is used to update email templates and store onto the database for Django Post office (optional)
	
	. Management command `populate_db` can be used to get dummy data (IMPORTANT)
	
	. Management command `jsonify_data` is used by atwho for data. Autogenerates some json objects which are easy to use
	
	. Management command `jsonify_data` is used to fix all permissions for the users in the beginning
	
6. Haystack and Solr
	. Commands  to install Solr:
	```curl -O https://archive.apache.org/dist/lucene/solr/3.5.0/apache-solr-3.5.0.tgz
	tar xvzf apache-solr-3.5.0.tgz
	cd apache-solr-3.5.0
	cd example
	java -jar start.jar```
	. Next, generate schema from ```python manage.py build_solr_schema```. Take the output from that command and place it in ```apache-solr-3.5.0/example/solr/conf/schema.xml```. Then restart Solr
	. Solr needs to be run continuously on server
	. Ref: http://django-haystack.readthedocs.org/en/latest/installing_search_engines.html


7. (specific to ERP)(Create a blank document called meta.html in files/templates/base/


8. Common Installation Problems

- At any point if you get permission denied type 'sudo' followed by the required command

8.a. - Details on how to set up MySQL Server. 
	
	To run the mysql prompt and create a database in the terminal type

		mysql -u root -p
		##Then type the root user password or set the password if it asks you to
		## The MySQL shell should open. type-  CREATE DATABASE django_db;
		## In settings.py under the database settings add 
		
	        'ENGINE':'django.db.backends.mysql',
        	'NAME': 'django_db',
        	'USER': 'root',
       		 'PASSWORD': whatever you set while creating the database,
       		 'HOST': '',
        	'PORT': '',
	- In terminal type 'python manage.py syncdb' followed by 'python manage.py migrate'. If these 2 worked your database settings worked fine	



8.b. For mysql installation problems

	- Type the all of the following commands to delete any version of mysql that you have

		sudo apt-get remove --purge mysql-server mysql-client mysql-common
		sudo apt-get autoremove
		sudo apt-get autoclean
	- To install mysql

		sudo apt-get install mysql-server mysql-client
		sudo apt-get install python-mysqldb
	- To run the mysql prompt and create a database

		mysql -u root -p
		##Then type the root user password or set the password if it asks you to
		## The MySQL shell should open. type-  CREATE DATABASE django_db;
		## In settings.py under the database settings add 
		
		'ENGINE':'django.db.backends.mysql',
        	'NAME': 'django_db',
        	'USER': 'root',
       		 'PASSWORD': whatever you set,
       		 'HOST': '',
        	'PORT': '',
	- In terminal type 'python manage.py syncdb' followed by 'python manage.py migrate'. If these 2 worked your database settings worked fine	

8.c. If pip is not installed check the following link

http://pip.readthedocs.org/en/latest/installing.html
		

8.d. If an older version of django is installed or you are unsure of the version. Type the following in terminal

	- python #(to enter python shell)
	- import django #(if youn get an error here, django is not installed)
	- print(django.get_version())

    if the version is 1.6.5 you are fine. If not then read on - you will have to delete and reinstall django. Tpe the following

	- python -c "import sys; sys.path = sys.path[1:]; import django; print(django.__path__)"
	- cd <type the output from the above command until the site-packages file only. e.g /....../sitepackages>
	- sudo rm -rf django
	- pip install Django==1.6.5
    Now repeat the steps till 'print(django.get_version())' to check your django version


8.e. static files are not loading Or the css files are not showing

	- set STATIC_URL to '/static/' in settings.py

8.f. Static(css/js) files are loading but not getting the shaastra/saarang logo on the login page

	- go to files/static/img/shaastra_pics Copy login_page_logo.jpg
	- go to files/static/img/ . Create a folder called fest_pics and paste the photo there (since the src attribute for that photo is files/static/img/fest_pics)


8.g. The following error is showing on the browser -  The storage backend of the staticfiles finder <class 'django.contrib.staticfiles.finders.DefaultStorageFinder'> doesn't have a valid location.

 	- In global_settings.py remove the following line in Staic_file_finders 'django.contrib.staticfiles.finders.DefaultStorageFinder',


8.h. Some Module like apiclient, south or any app mentioned in the Third-Party-Apps in globalsetings.py is not installed. 

	- Google 'install apiclient library' or whatever the module name is and type the command that you find in any of the results in terminal


------------------------------------------------------------------------------------------------------

Experimental Features :
 - Content Editable divs
