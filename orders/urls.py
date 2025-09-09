from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('coupon/', views.coupon, name='coupon'),
    path('payment/', views.payment, name='payment'),
    path('callback/', views.callback, name='callback'),

]