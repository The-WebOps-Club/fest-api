from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import User
from configs import settings
from apps.users.models import Dept, Subdept, Page, ERPProfile, UserProfile
from apps.walls.models import Wall, Post, Comment
import json
import os

class Command(BaseCommand):
    """
        Converts certain things to JSON for faster loading and less SQL hits :
            - User list : for Search - file="user_list.json"
            - Dept list : for Search - file="dept_list.json"
            - Subdept list : for Search - file="subdept_list.json"
            - Dept > Subdept > User dict : for contacts - file="user_structure.json"
            
    """
    help = 'Automatically adds required entries into the database. esp Departments and Walls for them.'

    def handle(self, arg=None, **options):

        static_files = settings.STATICFILES_DIRS[0]
        data_root = os.path.abspath(os.path.join(static_files, "json"))
        
        if not os.path.exists(data_root):
            os.makedirs(data_root)
        #- User list : for Search - file="user_list.json"
        user_list = list(User.objects.values("id", "first_name", "last_name"))
        user_list_file = os.path.abspath(os.path.join(data_root, "user_list.json"))

        with open(user_list_file, 'w') as outfile:
            json.dump(user_list, outfile)
        self.stdout.write("User ... done.")

        #- Subdept list : for Search - file="subdept_list.json"
        subdept_list = list(Subdept.objects.values("id", "name"))
        subdept_list_file = os.path.abspath(os.path.join(data_root, "subdept_list.json"))
        with open(subdept_list_file, 'w') as outfile:
            json.dump(subdept_list, outfile)
        self.stdout.write("Subdept ... done.")

        #- Dept list : for Search - file="dept_list.json"
        dept_list = list(Dept.objects.values("id", "name"))
        dept_list_file = os.path.abspath(os.path.join(data_root, "dept_list.json"))
        with open(dept_list_file, 'w') as outfile:
            json.dump(dept_list, outfile)
        self.stdout.write("Dept ... done.")

        #- Dept list : for Search - file="dept_list.json"
        dept_list = list(Page.objects.values("id", "name"))
        dept_list_file = os.path.abspath(os.path.join(data_root, "page_list.json"))
        with open(dept_list_file, 'w') as outfile:
            json.dump(dept_list, outfile)
        self.stdout.write("Page ... done.")

        #- Dept > Subdept > User dict : for contacts - file="user_structure.json"
        all_user_list = list(User.objects.values("id", "first_name", "last_name", "erp_profile","profile","email"))
        for i in all_user_list:
            if "erp_profile" in i.keys() and i["erp_profile"]:
                erp_prof = ERPProfile.objects.get(id=i["erp_profile"])
                i["coord_relations"] = erp_prof.coord_relations.values_list("id", flat="true")
                i["supercoord_relations"] = erp_prof.supercoord_relations.values_list("id", flat="true")
                i["core_relations"] = erp_prof.core_relations.values_list("id", flat="true")
                i["wall"] = erp_prof.wall.id

                del(i["erp_profile"])
            
            if "profile" in i.keys():
                if i["profile"]:
                    usr_prof = UserProfile.objects.get(id=i["profile"])
                    if (usr_prof.mobile_number):
                        i["mobile_number"]=usr_prof.mobile_number
                    else:
                        i["mobile_number"]="" 
                else:
                    i["mobile_number"]=""
                del(i["profile"])
        all_subdept_list = list(Subdept.objects.values("id", "name", "dept", "wall"))
        all_dept_list = list(Dept.objects.values("id", "name", "wall"))
        id_dept_structure = {}
        for i in all_dept_list:
            id_dept_structure[i["id"]] = {
                    "users" : {}, 
                    "subdepts": {},
                    "name" : i["name"]
                }
        id_subdept_structure = {}
        for i in all_subdept_list:
            id_subdept_structure[i["id"]] = {
                    "users" : {},
                    "name" : i["name"]
                } 

        for i in all_user_list:
            temp_user = {
                "first_name" : i["first_name"],
                "last_name" : i["last_name"],
                "email": i["email"],
                "mobile_number": i["mobile_number"],
            }
            if "coord_relations" in i.keys():
                for j in i["coord_relations"]:
                    id_subdept_structure[j]["users"][i["id"]] = temp_user
            if "supercoord_relations" in i.keys():
                for j in i["supercoord_relations"]:
                    id_dept_structure[j]["users"][i["id"]] = temp_user
            if "core_relations" in i.keys():
                for j in i["core_relations"]:
                    id_dept_structure[j]["users"][i["id"]] = temp_user
        for i in all_subdept_list:
            id_dept_structure[i["dept"]]["subdepts"][i["id"]] = id_subdept_structure[i["id"]]
        
        user_structure_file = os.path.abspath(os.path.join(data_root, "user_structure.json"))
        with open(user_structure_file, 'w') as outfile:
            json.dump(id_dept_structure, outfile)
        #print id_dept_structure
        self.stdout.write("Dept > Users + Subdepts > Users ... done.")

        self.stdout.write("All done")

