from django.urls import path, include

from products import views

app_name = 'products'

urlpatterns = [
    # Slider
    path('slider/', views.slider, name='slider'),
    path('home-slider/', views.home_slider, name='home_slider'),
    path('add-slider/', views.add_slider, name='add_slider'),
    path('update-slider/<int:pk>/', views.UpdateSlider.as_view(), name='update_slider'),

    # Category
    path('category/', views.category, name='category'),
    path('add-category/', views.add_category, name='add_category'),
    path('update-category/<int:pk>/', views.UpdateCategory.as_view(), name='update_category'),
    path('delete-category/<int:id>/', views.delete_category, name='delete_category'),

    # Product
    path('', views.home, name='home'),
    path('product/', views.product, name='product'),
    path('add-product/', views.add_product, name='add_product'),
    path('update-product/<int:pk>/', views.UpdateProduct.as_view(), name='update_product'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
]
