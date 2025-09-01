from django import forms

from orders.models import BillingAddress, Order


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo Code'
    }), required=False)


class CheckoutForm(forms.ModelForm):
    same_shipping_address = forms.BooleanField(required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    street_address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Name'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country Name'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City Name'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State Name'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post Code'}))
    s_street_address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Name'}))
    s_country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country Name'}))
    s_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City Name'}))
    s_state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State Name'}))
    s_zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post Code'}))
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    notes = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Notes about your order, e.g. special notes for delivery.'}),
        required=False)

    class Meta:
        model = BillingAddress
        fields = ['first_name', 'last_name', 'street_address', 'country',
                  'city', 'state', 'zip', 'same_shipping_address', 's_street_address',
                  's_country', 's_state', 's_city', 's_zip', 'phone_number',
                  'notes']



class OrderStatusForm(forms.ModelForm):
    order_status_choices = (
        ('DELIVERED', 'Order has been Delivered'),
        ('RECEIVED', 'Order Request Received',),
        ('REFUND', 'Apply for Refund',),
        ('GRANTED', 'Order Refund Granted',),
        ('UPDATE', 'Order Status Will Be Update Soon',),
    )
    order_status = forms.ChoiceField(label='Order Status', widget=forms.Select, choices=order_status_choices)

    class Meta:
        model = Order
        fields = ['order_status', ]

        widgets = {
            'order_status': forms.SelectMultiple(attrs={
                'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 '
                         'focus:outline-none focus:shadow-outline-purple dark:text-purple-300 '
                         'dark:focus:shadow-outline-gray'}),
        }