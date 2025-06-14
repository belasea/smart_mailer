# campaign/forms.py

from django import forms
from .models import EmailCampaign

class EmailCampaignForm(forms.ModelForm):
    class Meta:
        model = EmailCampaign
        fields = ['subject', 'message', 'recipients']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
