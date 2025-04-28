from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList, ResetPasswordForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'login.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            email = request.POST['email'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'login.html',
                          {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        user_form = CustomUserCreationForm()
        template_data['userForm'] = user_form
        return render(request, 'signup.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)

        if user_form.is_valid():
            user_form.save()
            return redirect('accounts.login')
        else:
            template_data['userForm'] = user_form
            return render(request, 'signup.html',
                          {'template_data': template_data})

def reset(request):
    template_data = {}
    template_data['title'] = 'Reset Password'
    if request.method == 'GET':
        form = ResetPasswordForm()
        template_data['userForm'] = form
        return render(request, 'reset.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        form = ResetPasswordForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            user = CustomUser.objects.get(username=form.cleaned_data['username'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('accounts.login')
        else:
            template_data['userForm'] = form
            return render(request, 'reset.html',
                          {'template_data': template_data})