from django.contrib import admin

# from myproject.product.models import Category

# Register your models here.
from .models import Category, Product

admin.site.register(Category)
admin.site.register(Product)
