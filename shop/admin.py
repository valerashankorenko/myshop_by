from django.contrib import admin
from .models import ParentCategory, Category, Product

admin.site.register(ParentCategory)
admin.site.register(Category)
admin.site.register(Product)
