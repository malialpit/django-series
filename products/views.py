from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from products.forms import CategoryForm
from products.models import Category


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
