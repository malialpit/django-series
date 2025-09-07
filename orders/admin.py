from django.contrib import admin

from orders.models import Cart, Order, BillingAddress, Coupon, OrderItem

# Register your models here.
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(BillingAddress)
admin.site.register(Coupon)
admin.site.register(OrderItem)