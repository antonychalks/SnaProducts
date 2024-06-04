from django.urls import path
from . import views

urlpatterns = [
    path('<int:list_id>', views.list_detail, name='list_detail'),
    path('create_list/', views.create_list, name='create_list'),
    # path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    # path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_list/<int:list_id>/', views.delete_list, name='delete_list'),
    # path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
]
