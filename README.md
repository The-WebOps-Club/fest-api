fest-api
========

An API implementation for Saarang Shaastra like fests, including ERP and Mainsite and Mobile interface

1. Setup :
	- Create a virtual env
	- Install configs/requirements.txt
		- use 
			```
			pip install -r config/requirements.txt
			```
		- and then to make sure of all versions
			```
			pip install -r config/requirements.txt --upgrade
			```
	- Modify configs/settings.sample.py to configs/settings.py with appropriate modifications


2. TastyPie :
    - Till now, tastypie(v1.11) has some issues with through tables. So this creates an error in the BloodRequest model creation as the through table gves an error.
    - Need to replace : 
     
     ```
     related_mngr.add(*related_objs)
     ```
      with :

            
            if hasattr(related_mngr, 'add'):
                related_mngr.add(*related_objs)
            else:
                # handle m2m with a "through" class
                for other_obj in related_objs:
                    related_mngr.through.objects.get_or_create(**{
                        related_mngr.source_field_name: bundle.obj,
                        related_mngr.target_field_name: other_obj
                    })
            
    in the save_m2m function ~line 2300

