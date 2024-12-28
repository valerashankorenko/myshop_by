from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/<int:category_id>/',
         views.product_list,
         name='product_list'),
    path('product/<int:product_id>/',
         views.product_detail,
         name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
]
