from django.urls import path
from . import views

urlpatterns = [
    path('<int:list_id>', views.list_detail, name='list_detail'),
    path('create_list/', views.create_list, name='create_list'),
    path('edit_list/<int:list_id>/', views.edit_list, name='edit_list'),
    path('delete_list/<int:list_id>/', views.delete_list, name='delete_list'),
    path('add_to_list/<int:product_id>/', views.add_to_list, name='add_to_list'),
]
