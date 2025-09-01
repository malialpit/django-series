from django.urls import path, include

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('admin-change-password/', views.admin_change_passsword, name='admin-change-password'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('admin-change-password/', views.admin_change_password, name='admin-change-password'),
    path('user-change-password/', views.user_change_password, name='user-change-password'),
]
