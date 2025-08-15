from django import forms
from products.models import Category


class CategoryForm(forms.ModelForm):
    is_active = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label='Category Availability Status')

    class Meta:
        model = Category
        fields = ['title', 'is_active']

        widgets = {
            'title': forms.TextInput(attrs={
                'class:': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                'placeholder': 'Category Name'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'text-purple-600 form-checkbox focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray',
            })
        }

        labels = {
            'title': 'Category Name',
        }
