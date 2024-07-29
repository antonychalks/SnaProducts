from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_products, name='products'),
    path('manage', views.manage_products, name='manage_products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
]
