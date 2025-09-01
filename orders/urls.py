from django.urls import path, include

from orders import views

app_name = 'orders'

urlpatterns = [
    path("checkout/", views.checkout_view, name="checkout"),
    path("coupon/", views.coupon, name="coupon"),
    path("payment/", views.payment, name="payment"),
    path("callback/", views.callback, name="callback"),
    path('generate-invoice/<int:order_id>/', views.GenerateInvoice.as_view(), name='generate_invoice'),
    path('manage-orders/', views.manage_orders, name='manage_orders'),
    path('order-status/<int:pk>/', views.UpdateOrderStatus.as_view(), name='order_status'),
    path('orders/', views.orders, name='orders'),
]
