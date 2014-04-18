#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from apps.portals.applications.coord.models import *

class AnswerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Answer, AnswerAdmin)

class CredentialAdmin(admin.ModelAdmin):
    pass
admin.site.register(Credential, CredentialAdmin)

class ReferenceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Reference, ReferenceAdmin)

class ApplicationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Application, ApplicationAdmin)

