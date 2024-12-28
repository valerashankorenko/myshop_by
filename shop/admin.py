from django.contrib import admin
from .models import ParentCategory, Category, Product


@admin.register(ParentCategory)
class ParentCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    ordering = ('id',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    list_display_links = ('id', 'name', 'parent')
    search_fields = ('id', 'name', 'parent__name')
    ordering = ('parent',)
    empty_value_display = '-пусто-'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'category')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'category__name')
    ordering = ('id', 'category',)
