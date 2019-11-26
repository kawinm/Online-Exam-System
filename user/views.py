from django.shortcuts import render, redirect

from user.models import Student
from .forms import LoginForm, RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('user:login')
    else:
        form = RegisterForm()
        return render(request, 'user/register.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            email_id = data.get('email_id')
            password_entered = data.get('password')

            smail = Student.objects.filter(email_id__iexact=email_id, )
            password = smail.values('password')
            
            for word in password:
                if password_entered == word['password']:
                    response = redirect('exam:main')
                    response.set_cookie('username', email_id)
                    return response
            return redirect('user:login')
    else:
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

