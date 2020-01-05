from django import forms

from .models import Student

class RegisterForm(forms.ModelForm):

    #Conditions added to ensure these fields contain only alphanumeric character and autocomplete off
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '}))
    
    #To make Password field not visible use PasswordInput()
    password = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'id': 'password','autocomplete': 'off'}))
    
    class Meta:
        model = Student
        fields = ('first_name', 'last_name','year','email_id', 'password',)


class LoginForm(forms.ModelForm):

    #To make Password field not visible use PasswordInput()
    password = forms.CharField(required=True,widget=forms.PasswordInput())

    class Meta:
        model = Student
        fields = ('email_id', 'password',)