from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'date_of_birth',
            'gender',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        user.is_active = True
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email', 
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

  
# User Update Form ===========================
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'gender',
            'profile',
            'date_of_birth',
            'contact_number',
        ]
