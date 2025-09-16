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
    street_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Name'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip'}))
    s_street_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}))
    s_country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))
    s_state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    s_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}))
    s_zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zi['}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    notes = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notes about your order'}), required=False)


    class Meta:
        model = BillingAddress
        exclude = ['user', ]


class OrderStatusForm(forms.ModelForm):
    STATUS = (
        ('DELIVERED', 'Order has been Delivered'),
        ('RECEIVED', 'Order request Received'),
        ('REFUND', 'Apply for Refund'),
        ('GRANTED', 'Order Refund Granted'),
        ('UPDATE', 'Order Status Will Be Update Soon'),
    )
    order_status = forms.ChoiceField(label='Order Status', widget=forms.Select, choices=STATUS)

    class Meta:
        model = Order
        fields = ['order_status', ]

        widgets = {
            'order_status': forms.SelectMultiple(attrs={
                'class:': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            }),
        }