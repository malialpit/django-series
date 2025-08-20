from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML
from django import forms
from products.models import Category, Product, Slider


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


class ProductForm(forms.ModelForm):
    Options = (
        ('B', 'Best Seller'),
        ('S', 'Sale'),
        ('N', 'New'),
        ('T', 'Top Rate'),
    )
    label = forms.ChoiceField(label='Product Tag', widget=forms.Select, choices=Options)
    is_active = forms.BooleanField(widget=forms.CheckboxInput(), required=False, label='Product Availability Status')

    class Meta:
        model = Product
        fields = ['title', 'price', 'discount_price', 'category', 'label',
                  'description', 'image', 'side_image_1', 'side_image_2', 'is_active']

        widgets = {
            'title': forms.TextInput(attrs={
                'class:': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                'placeholder': 'Product Name'
            }),
            'price': forms.NumberInput(attrs={
                'class:': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                'placeholder': 'Product Price'
            }),
            'discount_price': forms.NumberInput(attrs={
                'class:': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                'placeholder': 'Discount Price'
            }),
            'label': forms.SelectMultiple(attrs={
                'class:': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            }),
            'description': forms.Textarea(attrs={
                'class:': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                'placeholder': 'Product Description'
            }),
            'image': forms.FileInput(attrs={
                'class:': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            }),
            'side_image_1': forms.FileInput(attrs={
                'class:': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            }),
            'side_image_2': forms.FileInput(attrs={
                'class:': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'text-purple-600 form-checkbox focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray',
            })
        }

        labels = {
            'title': 'Product Name',
            'price': 'Price',
            'discount_price': 'Discount Price',
            'category': 'Product Category',
            'description': 'Description',
            'image': 'Product Image',
            'side_image_1': 'Product Side Image 1',
            'side_image_2': 'Product Side Image 2',
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = False
            self.helper.use_custom_control = False
            self.helper.layout = Layout(
                'title',
                'price',
                'discount_price',
                'category',
                'label',
                'description',
                'image',
                HTML("<p style=color:white;>product image: {{image}}</p>"),
                HTML("<br/>"),
                'side_image_1',
                HTML("<br/>"),
                HTML("<p style=color:white;>product side image 1: {{side_image_1}}</p>"),
                'side_image_2',
                HTML("<p style=color:white;>product side image 2: {{side_image_2}}</p>"),
                HTML("<br/>"),
                'is_active'

            )


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['slide_1', 'slide_2', 'slide_3']

        widgets = {
            'slide_1': forms.FileInput(attrs={
                'class:': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            }),
            'slide_2': forms.FileInput(attrs={
                'class:': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            }),
            'slide_3': forms.FileInput(attrs={
                'class:': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            }),

        }

        labels = {
            'slide_1': 'Slider 1',
            'slide_2': 'Slider 2',
            'slide_3': 'Slider 3',

        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = False
            self.helper.use_custom_control = False
            self.helper.layout = Layout(
                'slide_1',
                HTML("<p style=color:white;>slider image 1: {{slide_1}}</p>"),
                HTML("<br/>"),
                'slide_2',
                HTML("<br/>"),
                HTML("<p style=color:white;>slider image 2: {{slide_2}}</p>"),
                'slide_3',
                HTML("<p style=color:white;>slider image 3: {{slide_3}}</p>"),
                HTML("<br/>"),

            )