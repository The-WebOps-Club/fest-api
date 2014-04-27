"""
WSGI config for fest_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import site
import __future__
# Paths
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VENV_FILE = os.path.abspath(os.path.join(ROOT_PATH, 'venv', 'bin', 'activate_this.py'))
PAKG_PATH = os.path.abspath(os.path.join(ROOT_PATH, 'venv', 'lib', 'python2.7', 'site-packages'))

# Add virtual environment to site directories:
site.addsitedir(ROOT_PATH)

# handle the path variable
path = [
   ROOT_PATH,
    os.path.abspath(os.path.join(ROOT_PATH, 'configs')),
    os.path.abspath(os.path.join(ROOT_PATH, 'venv')),
    os.path.abspath(os.path.join(ROOT_PATH, 'venv', 'bin')),
    os.path.abspath(os.path.join(ROOT_PATH, 'venv', 'lib')),
    os.path.abspath(os.path.join(ROOT_PATH, 'venv', 'lib', 'python2.7')),
    PAKG_PATH
    ]
#while len(sys.path) :
#    sys.path.pop(0)
for i in path: # If path exists, remove and add on the top
    if i not in sys.path:
        sys.path.insert(0, i)
    else:
        while i in sys.path:
            sys.path.remove(i)
        sys.path.insert(0, i)

#print sys.path
#raise Exception(sys.path)

execfile(VENV_FILE, dict(__file__=VENV_FILE))

# Switch to the directory of your project. (Optional)
os.chdir(ROOT_PATH)

# Set the DJANGO_SETTINGS_MODULE environment variables
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
