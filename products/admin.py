from django.contrib import admin
from .models import Product, Brand, Category, Offer, ProductImages, Review

# Register your models here.

admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Offer)
admin.site.register(ProductImages)
admin.site.register(Review)
