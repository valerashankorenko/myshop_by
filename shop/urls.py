from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('',
         views.CategoryListView.as_view(),
         name='index'),
    path('category/<int:category_id>/',
         views.ProductListView.as_view(),
         name='product_list'),
    path('product/<int:product_id>/',
         views.ProductDetailView.as_view(),
         name='product_detail'),
    path('add_to_cart/<int:product_id>/',
         views.CartCreateView.as_view(),
         name='add_to_cart'),
    path('cart/',
         views.CartListView.as_view(),
         name='view_cart'),
    path('cart/delete/<int:pk>/',
         views.CartItemDeleteView.as_view(),
         name='cart_item_delete'),
    path('cart/clear/',
         views.ClearCartView.as_view(),
         name='clear_cart'),
    path('cart/increase/<int:item_id>/',
         views.CartIncreaseView.as_view(),
         name='increase_quantity'),
    path('cart/decrease/<int:item_id>/',
         views.CartDecreaseView.as_view(),
         name='decrease_quantity'),
]
