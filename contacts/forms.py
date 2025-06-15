import re
from django import forms
from django.forms import Textarea
from .models import Contact, ReplayContact

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

 # ContactForm ==============================================
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'subject',
            'name',
            'phone',
            'email',
            'message',
        ]
        widgets = {
            'message': Textarea(attrs={'rows': 3, 'cols': 3}),
        }
    
    # Validation ===========================================
    def clean_name(self):
        name = self.cleaned_data.get("name")
        
        if name.lower() == "hi" or isinstance(name, int):
            raise forms.ValidationError("Please provide a valid name")
        
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError('Invalid email format')
        
        return email

 # ReplayContactForm ======================
class ReplayContactForm(forms.ModelForm):
    class Meta:
        model = ReplayContact
        fields = [
            'replay',
            'message',
        ]
        # Override the Customer some fields
        widgets = {
            'message': Textarea(attrs={'rows': 4, 'cols': 4 }),
        }