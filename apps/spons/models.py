from django.db import models
from django.contrib.auth.models import User

class SponsImageUpload(models.Model):
    title = models.CharField(max_length=1000,verbose_name='Title',help_text='Example:Title Sponsor, Website Sponsor')
    sponsor_link = models.URLField(max_length=500, help_text='Example: http://company.com')
    logo = models.ImageField(upload_to='spons')
    timestamp = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, related_name='image_uploaded_by')
    priority = models.FloatField(default=0.00, help_text='Rate in a scale of 00.00000000 to 99.99999999. Highest number will appear first.')

    class Meta:
        permissions = (
            ('manage_logo', 'Can manage logos'),
            )
