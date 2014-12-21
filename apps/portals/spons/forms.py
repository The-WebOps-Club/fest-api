from apps.spons.models import SponsImageUpload
from django import forms

class AddLogoForm(forms.ModelForm):
    class Meta:
        model = SponsImageUpload
        exclude = ['timestamp', 'uploaded_by']
        help_texts = {
            'title': ('Example:Title Sponsor, Website Sponsor'),
        }