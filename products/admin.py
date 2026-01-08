from django.contrib import admin
from .models import Product, Brand, Category, Offer, ProductImages, Review, BundleItem

# Register your models here.

class BundleItemInline(admin.TabularInline):
    model = BundleItem
    fk_name = 'bundle'
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'current_price', 'active', 'quantity', 'flag']
    list_filter = ['active', 'product_type', 'flag', 'brand', 'category']
    search_fields = ['name', 'sku', 'subtitle', 'descriptions']
    filter_horizontal = ['category']
    inlines = [BundleItemInline]
    readonly_fields = ['calculated_bundle_price']
    
    def current_price(self, obj):
        return obj.new_price
    current_price.short_description = 'Price'

    def calculated_bundle_price(self, obj):
        return obj.bundle_total_price()
    calculated_bundle_price.short_description = 'Calculated Bundle Price'

class ProductCategoryInline(admin.TabularInline):
    model = Product.category.through
    extra = 1
    autocomplete_fields = ['product']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    inlines = [ProductCategoryInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Offer)
admin.site.register(ProductImages)
admin.site.register(Review)
admin.site.register(BundleItem)

