from django.contrib import admin

from orders.models import Order, Cart, BillingAddress, Coupon, OrderItem, Payment, Transaction

# Register your models here.
admin.site.register(Cart)
admin.site.register(BillingAddress)
admin.site.register(Coupon)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Transaction)