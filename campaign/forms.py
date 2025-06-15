from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import EmailCampaign

class EmailCampaignForm(forms.ModelForm):
    class Meta:
        model = EmailCampaign
        fields = '__all__'
        widgets = {
            'message': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '300px',  # Adjust the height as needed
                }
            }),
            
            'recipients': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter comma-separated emails'
            }),
        }
