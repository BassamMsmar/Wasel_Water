import os
from PIL import Image
from io import BytesIO
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.db.models.aggregates import Avg
from .utils import convert_image_to_webp

FLAG_TYPES = (
    ('sale', 'sale'),
    ('new', 'new'),
    ('feature', 'feature'),
)

PRODUCT_TYPES = (
    ('single', 'منتج أساسي مفرد'),
    ('bundle', 'عرض مجمّع'),
)
# Create your models here.
class Product(models.Model):
    name = models.CharField(_("Name"), max_length=120)
    flag = models.CharField(_("Flag"),max_length=10, choices=FLAG_TYPES)    
    image = models.ImageField(_("Image"), upload_to='products', default='products/default.jpg')
    old_price  = models.FloatField(_("Old Price") , default=0)
    new_price = models.FloatField(_("New Price"), default=0)
    linkVideo = models.CharField(_("Link Video"), max_length=100, null=True, blank=True)
    sku = models.CharField(_("Sku"), max_length=50, null=True, blank=True)
    subtitle = models.CharField(_("Subtitle"), max_length=300, null=True, blank=True)
    descriptions = models.TextField(_("Descriptions"), max_length=40000, null=True, blank=True)
    quantity = models.IntegerField(_("Quantity"))
    brand = models.ForeignKey("Brand", verbose_name=('Brand'), related_name='product_brand', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ManyToManyField("Category", verbose_name=('Category'), related_name='product_category', null=True)
    slug = models.SlugField(_("Slug"), null=True, blank=True)
    active = models.BooleanField(_("Active"), default=True)
    create_at = models.DateTimeField(_("Create at"), default=timezone.now, null=True, blank=True)
    product_type = models.CharField(_("Product Type"), max_length=10, choices=PRODUCT_TYPES, default='single')
    sales_count = models.IntegerField(_("Sales Count"), default=0)
    tags = TaggableManager()    


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(Product, self).save(*args, **kwargs)

        if self.image:
            img_path = self.image.path
            webp_path = convert_image_to_webp(img_path)

            # Delete the original image after conversion
            if os.path.exists(img_path):
                os.remove(img_path)

            webp_rel_path = f'products/{os.path.basename(webp_path)}'
            self.image.name = webp_rel_path
            super().save(update_fields=['image'])


    @property
    def is_bundle(self):
        return self.product_type == 'bundle'

    def bundle_total_price(self):
        if not self.is_bundle:
            return self.new_price
        total = 0
        for item in self.bundle_items.all():
            total += item.quantity * item.price_in_bundle
        return total

    def bundle_base_price(self):
        if not self.is_bundle:
            return 0
        total = 0
        for item in self.bundle_items.all():
            total += item.quantity * item.item.new_price
        return total

    def bundle_discount(self):
        return self.bundle_base_price() - self.bundle_total_price()

    def __str__(self) -> str:
            return self.name
    


class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='product_image', verbose_name=_("Product"), on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to='product_images')

    def __str__(self) -> str:
                return str(self.product) # Fixed typo self.products -> self.product


class Brand(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    image = models.ImageField(_("Images"), upload_to='brand')
    slug = models.SlugField(_("Slug"), null=True, blank=True)


    def __str__(self) -> str:
            return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(Brand, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    image = models.ImageField(_("Images"), upload_to='Category')
    slug = models.SlugField(_("Slug"), null=True, blank=True)

    def __str__(self) -> str:
            return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)


class Offer(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"), max_length=40000, null=True, blank=True)
    image = models.ImageField(_("Image"), upload_to='offers')
    products = models.ForeignKey(Product, related_name='offers_product', verbose_name=_("Product"), on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
            return self.title

class Review(models.Model):
    user = models.ForeignKey(User, verbose_name=('User'), related_name='rebiew_user', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, related_name='review_product', verbose_name=_("Product"), on_delete=models.SET_NULL, null=True)
    rate = models.IntegerField(_("Rate"))
    review = models.CharField(_("Review"), max_length=300)
    create_at = models.DateTimeField(_("Create at"), default=timezone.now)


    def __str__(self) -> str:
            return f"{self.user} - {self.product}"

class BundleItem(models.Model):
    bundle = models.ForeignKey(Product, related_name='bundle_items', verbose_name=_("Bundle"), on_delete=models.CASCADE)
    item = models.ForeignKey(Product, related_name='included_in_bundles', verbose_name=_("Item"), on_delete=models.CASCADE)
    quantity = models.IntegerField(_("Quantity"), default=1)
    price_in_bundle = models.FloatField(_("Price in Bundle"), default=0)

    class Meta:
        unique_together = ('bundle', 'item')

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in {self.bundle.name}"

    def save(self, *args, **kwargs):
        # Auto-set price_in_bundle to original price if 0 on creation
        if self.price_in_bundle == 0 and self.item:
            self.price_in_bundle = self.item.new_price
        super().save(*args, **kwargs)