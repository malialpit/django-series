from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from accounts.forms import SignUpForm


# Create your views here
@login_required
def dashboard(request):
    return render(request, 'base/base.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
        # else:
        #     return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                request.session.set_expiry(3600)
                if user.is_admin:
                    return redirect('accounts:dashboard')
                else:
                    return redirect('accounts:dashboard')
            else:
                messages.info(request, 'Username OR Password is Incorrect !')

    return render(request, 'registration/login.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def admin_change_passsword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password changed", extra_tags='green')
            return redirect('accounts:dashboard')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'registration/password-change-form.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(settings.LOGIN_URL)