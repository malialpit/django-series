from time import sleep

from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from products.models import Product


# Create your models here.
class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Cart(TimeStamp):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_discount_product_price(self):
        return self.quantity * self.product.discount_price

    def get_discount_product_price(self):
        return self.product.discount_price

    @property
    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_product_price()
        return self.get_total_product_price()


class BillingAddress(TimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)
    country = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    zip = models.CharField(max_length=40)
    s_street_address = models.CharField(max_length=200)
    s_country = models.CharField(max_length=40)
    s_city = models.CharField(max_length=40)
    s_zip = models.CharField(max_length=40)
    phone_number = PhoneNumberField()
    notes = models.TextField(max_length=100, blank=True, null=True)
    same_shipping_address = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name




class Coupon(TimeStamp):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Order(TimeStamp):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    STATUS = (
         ('DELIVERED', 'Order has been Delivered'),
         ('RECEIVED', 'Order request Received'),
         ('REFUND', 'Apply for Refund'),
         ('GRANTED', 'Order Refund Granted'),
         ('UPDATE', 'Order Status Will Be Update Soon'),
    )
    order_status = models.CharField(choices=STATUS, default='UPDATE', max_length=50)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'ORDKF{self.order_id}'

    @property
    def get_subtotal(self):
        return sum(item.get_total_item_price() for item in self.order_items.all())

    @property
    def get_discount(self):
        return self.coupon.amount if self.coupon else 0

    @property
    def get_total(self):
        subtotal = self.get_subtotal - self.get_discount
        return subtotal



class OrderItem(TimeStamp):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'ORDKF{self.order.order_id}'

    def get_total_item_price(self):
        return self.quantity * self.product.discount_price

    def get_coupon_discount(self):
        if self.order.coupon:
            return self.order.coupon.amount
        return 0

    def get_final_price(self):
        total = self.get_total_item_price()
        discount = self.get_coupon_discount()
        return total - discount if discount else total

