Fest-API
========

An API implementation for Saarang Shaastra like fests, including ERP and Mainsite and Mobile interface

1. Setup :
	- Check your dependencies
		- You need python 2.7.x+ and django 1.6.5 to use this. You can check it with :
		```
			# python -c "import django; print(django.get_version())"
		```
			If it gives `1.6.5` Then continue. Else, uninstall and reinstall django
		- Install pip using [this](http://pip.readthedocs.org/en/latest/installing.html)
		- Install 
		```
			python-virtualenv libmysqlclient-dev python-dev mysql-server mysql-client
		```
	- Create a virtual env
		- Go into the folder of the git repository and use `virtualenv --no-site-packages venv`
		- If you do not know what git repository means read [this](http://rogerdudler.github.io/git-guide/) for a beginner crash course
		- If you do not know what python-virtualenv means read [this](http://www.pythonforbeginners.com/basics/python-virtualenv-usage)
	- Install configs/requirements.txt
		- use 
			```
			pip install -r configs/requirements.txt (read 8.c if pip is not installed. 
			```
		- and then to make sure of all versions
			```
			pip install -r configs/requirements.txt --upgrade
			```
2. Changes required - which are in gitignore
	- Create a file named conigs/settings.py anf copy everything from config/settings.sample.py. Change the following in the fest-api/configs/settings.py
		- Set the database settings. Use the following to create a database :
		```
			# mysql -u root -p
			mysql> CREATE DATABASE fest_api_db;
		```
		Change the DATABASE lines in settings.py to :
		```
			'ENGINE':'django.db.backends.mysql',
        	'NAME': 'fest_api_db',
    	    'USER': 'root',
         	'PASSWORD': '<YOUR_PASSWORD>',
         	'HOST': '',
        	'PORT': '',
		```
		- In globalsettings.py set 'USE_EXTERNAL_SITES' to False - This will disable google docs for now
		- In terminal type 'python manage.py syncdb' followed by 'python manage.py migrate'.
	- Create a blank document called meta.html in files/templates/base/


3. Setup Database :
 
	- Management command `populate_db` can be used to get dummy data (IMPORTANT)
	
	- Management command `add_colleges` is used to populate some data - Colleges from Shaastra 2014 (optional) (In other words type 'python manage.py add_colleges')

	- Management command `update_email_templates` is used to update email templates and store onto the database for Django Post office (optional)
	
	- Management command `jsonify_data` is used by atwho for data. Autogenerates some json objects which are easy to use
	
	- Management command `fix_permissions` is used to fix all permissions for the users in the beginning

4. Setup Social Accounts : (NOT REQUIRED)

	- FACEBOOK
		- Add your facebook credentials (token, key) into settings

	- GOOGLE
		- Go to `{{SITE_URL}}/docs/refresh_token` to create a new refresh token.
		- This will ask access to a Google account - use the account on which to store Docs and accept.
		- Now this will store the refresh_token in a configs file and ask you to restrat server.
		- Restart Server to refetch all settings.
		- Now you can access Google Drive and Google Picker API
		
		- Also, add google credentials into settings
			- Google Public Key
			- Google oauth configs into configs/docs_oauth2_credentials.json
	
5. Search using Solr (NOT REQUIRED)

	- Commands  to install Solr:
		```
		curl -O https://archive.apache.org/dist/lucene/solr/3.5.0/apache-solr-3.5.0.tgz
		tar xvzf apache-solr-3.5.0.tgz
		cd apache-solr-3.5.0
		cd example
		java -jar start.jar
		```
	- Next, generate schema from 
		```
		python manage.py build_solr_schema
		```
	- Take the output from that command and place it in 
		```
		apache-solr-3.5.0/example/solr/conf/schema.xml
		```
	- Then restart Solr : Solr will be continuously running on server, like Apache
	- [Reference](http://django-haystack.readthedocs.org/en/latest/installing_search_engines.html)

6. Common Installation Problems
	- At any point if you get permission denied type 'sudo' followed by the required command

	a. Static files are not loading Or the css files are not showing - set STATIC_URL to '/static/' in settings.py

	b. If you get the error meta.html not found - set STATIC_URL to '/static/' in settings.py

	c. Static(css/js) files are loading but not getting the shaastra/saarang logo on the login page
		- copy `files/static/img/shaastra_pics` to `files/static/img/fest_pics` or `files/static/img/saarang_pics` to `files/static/img/fest_pics`

	d. Some Module like apiclient, south or any app mentioned in the Third-Party-Apps in globalsetings.py is not installed. 

		- Google 'install apiclient library' or whatever the module name is and type the command that you find in any of the results in terminal
