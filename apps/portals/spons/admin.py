from django.contrib import admin

from apps.spons.models import SponsImageUpload

class SponsImageUploadAdmin(admin.ModelAdmin):
    list_display=('priority', 'title', 'sponsor_link', 'logo', 'timestamp', 'uploaded_by')
    search_fields = ['title', 'sponsor_link']

admin.site.register(SponsImageUpload, SponsImageUploadAdmin)