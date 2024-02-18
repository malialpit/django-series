from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from accounts.forms import SignUpForm


# Create your views here
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
            return redirect('account:login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
