from django.urls import path, include

from products import views

app_name = 'products'

urlpatterns = [
    # Category app
    path('category/', views.category, name='category'),
    path('add-category/', views.add_category, name='add_category'),
    path('update-category/<int:pk>/', views.UpdateCategory.as_view(), name='update_category'),
    path('delete-category/<int:id>/', views.delete_category, name='delete_category'),
]
