from django.shortcuts import render, redirect
from django.http import HttpResponse

from user.models import Student
from .forms import LoginForm, RegisterForm

from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .register.token import account_activation_token

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            
            # Saving registered value
            post = form.save()
            post.is_active = True
            post.save()

            #Sending confirmation mail 
            """ current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('user/acc_active_email.html', {
                    'user': post,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(post.pk)),
                    'token':account_activation_token.make_token(post),
            })
            to_email = form.cleaned_data.get('email_id')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration') """
            return redirect('admin:index')
        else:
            message = 'Email id is already registered.'
            form = RegisterForm()
            return render(request, 'user/register.html', {'form': form, 'message':message})
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
            message = "Incorrect Email id or Password"
            form = LoginForm()
            return render(request, 'user/login.html', {'form': form, 'message':message})
        return redirect('user:login')
    else:
        if 'username' not in request.COOKIES:
            form = LoginForm()
            return render(request, 'user/login.html', {'form': form})
        else:
            return redirect('exam:main')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Student.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('user:login')
    else:
        return HttpResponse('Activation link is invalid!')

def logout(request):
    response = redirect('user:login')
    response.delete_cookie('username')
    return response