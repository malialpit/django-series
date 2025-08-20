import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from products.forms import CategoryForm, ProductForm, SliderForm
from products.models import Category, Product, Slider


# Create your views here.
@login_required
def category(request):
    categories = Category.objects.filter(is_deleted=False).order_by('id')
    paginator = Paginator(categories, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'categories': categories, 'page_obj': page_obj}
    return render(request, 'products/category.html', context)


@login_required()
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:category')
    else:
        form = CategoryForm()
    return render(request, 'products/add-category.html', {'form': form})


class UpdateCategory(LoginRequiredMixin, generic.UpdateView):
    model = Category
    template_name = 'products/edit-category.html'
    form_class = CategoryForm
    login_url = '/login/'
    success_url = reverse_lazy('products:category')


@login_required()
def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete_category()
    return redirect('products:category')


def home(request):
    products = Product.objects.filter(is_active=True, is_deleted=False).order_by('id')
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'products': products, 'page_obj': page_obj}
    return render(request, 'products/home.html', context)


@login_required()
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products:product')
    else:
        form = ProductForm()
    return render(request, 'products/add-product.html', {'form': form})


@login_required
def product(request):
    products = Product.objects.filter(is_active=True, is_deleted=False).order_by('id')
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'products': products, 'page_obj': page_obj}
    return render(request, 'products/product.html', context)


class UpdateProduct(LoginRequiredMixin, generic.UpdateView):
    model = Product
    template_name = 'products/edit-product.html'
    form_class = ProductForm
    login_url = '/login/'
    success_url = reverse_lazy('products:product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['image'] = os.path.basename(product.image.name)
        context['side_image_1'] = os.path.basename(product.side_image_1.name)
        context['side_image_2'] = os.path.basename(product.side_image_2.name)
        return context


@login_required()
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete_product()
    return redirect('products:product')


@login_required()
def add_slider(request):
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products:slider')
    else:
        form = SliderForm()
    return render(request, 'products/add-slider.html', {'form': form})


@login_required
def slider(request):
    sliders = Slider.objects.all()
    context = {'sliders': sliders,}
    return render(request, 'products/slider.html', context)


def home_slider(request):
    sliders = Slider.objects.all()
    context = {'sliders': sliders,}
    return render(request, 'user/slider.html', context)


class UpdateSlider(LoginRequiredMixin, generic.UpdateView):
    model = Slider
    template_name = 'products/edit-slider.html'
    form_class = SliderForm
    login_url = '/login/'
    success_url = reverse_lazy('products:slider')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slider = self.object
        context['slide_1'] = os.path.basename(slider.slide_1.name)
        context['slide_2'] = os.path.basename(slider.slide_2.name)
        context['slide_3'] = os.path.basename(slider.slide_3.name)
        return context
