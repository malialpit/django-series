from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from accounts.forms import SignUpForm, ContactForm
from orders.models import Transaction, Order
from products.models import Product


# Create your views here
@login_required
def dashboard(request):
    product = Product.objects.filter(is_active=True, is_deleted=False).order_by('id')
    balance = Transaction.objects.filter(payment_status=1)
    sale = Order.objects.filter(order_status='DELIVERED')
    delivery = Order.objects.filter(order_status='UPDATE')
    total_product = product.count()
    total_balance = sum(t.payment.order.get_total for t in balance)
    total_sale = sale.count()
    total_deliveries = delivery.count()
    context = {'total_product': total_product, 'total_balance': total_balance, 'total_sale': total_sale,
               'total_deliveries': total_deliveries}
    return render(request, 'accounts/dashboard.html', context)


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

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:contact')
    else:
        form = ContactForm()
    return render(request, 'user/contact.html', {'form': form})

def about(request):
    return render(request, 'user/about.html')

def admin_change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Password Changed", extra_tags='green')
            return redirect('accounts:dashboard')
    else:
        form = PasswordChangeForm(user=request.user)
    context = {'form': form}
    return render(request, 'registration/password-change-form.html', context)


def user_change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Password Changed", extra_tags='green')
            return redirect('products:home')
    else:
        form = PasswordChangeForm(user=request.user)
    context = {'form': form}
    return render(request, 'registration/user-password-change-form.html', context)
