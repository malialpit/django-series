from django import forms
from django.core.exceptions import ValidationError

from accounts.models import User


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 '
                 'focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray '
                 'form-input',
        'placeholder': 'Enter Your Password'}))
    password2 = forms.CharField(label='Confirm Password again', widget=forms.PasswordInput(attrs={
        'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 '
                 'focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray '
                 'form-input',
        'placeholder': 'Re-Confirm Your Password'}))
    error_messages = {'is_agree': {'required': 'Please accept our privacy policy.'}}

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'is_agree']
        widgets = {
            'first_name' : forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 '
                         'focus:outline-none focus:shadow-outline-purple dark:text-gray-300 '
                         'dark:focus:shadow-outline-gray'
                         'form-input',
                'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 '
                         'focus:outline-none focus:shadow-outline-purple dark:text-gray-300 '
                         'dark:focus:shadow-outline-gray'
                         'form-input',
                'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 '
                         'focus:outline-none focus:shadow-outline-purple dark:text-gray-300 '
                         'dark:focus:shadow-outline-gray'
                         'form-input',
                'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 '
                         'focus:outline-none focus:shadow-outline-purple dark:text-gray-300 '
                         'dark:focus:shadow-outline-gray'
                         'form-input',
                'placeholder': 'example +91 1234567890'}),
            'is_agree': forms.CheckboxInput(attrs={
                'class': 'text-purple-600 form-checkbox focus:border-purple-400 focus:outline-none '
                         'focus:shadow-outline-purple dark:focus:shadow-outline-gray',
                'style': 'background-color: purple;',
                'required': 'Please accept our privacy & policy.'}),

        }

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'is_agree': 'I Agree to Terms & Conditions'
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password doesn't match")
        return password2

    def clean_username(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already exists")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

