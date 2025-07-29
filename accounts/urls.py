from django.urls import path, include

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('', views.signup, name='signup'),
    path('admin-change-password/', views.admin_change_password, name='admin-change-password'),
]
