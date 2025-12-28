from django import forms
from django.contrib.auth import get_user_model
from .models import USER_TYPE_CHOICES, Job, CustomUser

User = get_user_model()

class RegisterForm(forms.ModelForm):
    display_name = forms.CharField(max_length=50, required=True, help_text='First Name')
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'display_name', 'email', 'user_type', 'company_name', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['display_name']
        user.email = self.cleaned_data['email']
        user.user_type = self.cleaned_data['user_type']
        user.company_name = self.cleaned_data.get('company_name')
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['company_name']
        
class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['skills', 'resume']

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'number_of_openings', 'category', 'description', 'skills_required']
