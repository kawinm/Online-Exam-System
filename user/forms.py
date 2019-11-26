from django import forms

from .models import Student

class RegisterForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name','year','email_id', 'password',)

class LoginForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('email_id', 'password',)