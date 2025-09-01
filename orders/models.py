from django.db import models
from django.conf import settings
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from products.models import Product, TimeStamp


# Create your models here.


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


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=100)
    country = models.CharField(max_length=40)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    s_street_address = models.CharField(max_length=100)
    s_country = models.CharField(max_length=40)
    s_city = models.CharField(max_length=100)
    s_state = models.CharField(max_length=100)
    s_zip = models.CharField(max_length=100)
    phone_number = PhoneNumberField(null=True)
    notes = models.TextField(max_length=100, blank=True, null=True)
    same_shipping_address = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = 'BillingAddresses'


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Order(TimeStamp):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    order_status_choices = (
        ('DELIVERED', 'Order has been Delivered'),
        ('RECEIVED', 'Order Request Received',),
        ('REFUND', 'Apply for Refund',),
        ('GRANTED', 'Order Refund Granted',),
        ('UPDATE', 'Order Status Will Be Update Soon',),
    )
    order_status = models.CharField(choices=order_status_choices, default='UPDATE', max_length=50)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'ORDKSF{self.order_id}'

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
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'ORDKSF{self.order.order_id}'

    def get_total_item_price(self):
        return self.quantity * self.product.discount_price

    def get_coupon_discount(self):
        if self.order.coupon:
            # distribute discount per item (simple version)
            return self.order.coupon.amount
        return 0

    def get_final_price(self):
        total = self.get_total_item_price()
        discount = self.get_coupon_discount()  # must use ()
        return total - discount if discount else total


class Payment(TimeStamp):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    merchant_id = models.CharField(max_length=100)
    merchant_transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.merchant_id}"


class Transaction(TimeStamp):
    transaction_id = models.AutoField(primary_key=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE'),
        (3, 'PENDING'),
    )
    payment_status = models.CharField(choices=payment_status_choices, default=2, max_length=4)
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    datetime_of_payment = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_id}"
