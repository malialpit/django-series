from django import forms

from orders.models import BillingAddress


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