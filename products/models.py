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
    category = models.ForeignKey("Category", verbose_name=('Category'), related_name='product_category', on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(_("Slug"), null=True, blank=True)
    active = models.BooleanField(_("Active"), default=True)
    create_at = models.DateTimeField(_("Create at"), default=timezone.now, null=True, blank=True)
    product_type = models.CharField(_("Product Type"), max_length=10, choices=PRODUCT_TYPES, default='single')
    tags = TaggableManager()    


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
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


    # def ave_rate(self):
    #       avg = self.review_product.aggregate(rate_ave=Avg('rate'))
    #       return avg['rate_ave']
    
    def __str__(self) -> str:
            return self.name
    



class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='product_image', verbose_name=_("Product"), on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to='product_images')

    def __str__(self) -> str:
                return str(self.products)


class Brand(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    image = models.ImageField(_("Images"), upload_to='brand')
    slug = models.SlugField(_("Slug"), null=True, blank=True)


    def __str__(self) -> str:
            return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    image = models.ImageField(_("Images"), upload_to='Category')
    slug = models.SlugField(_("Slug"), null=True, blank=True)

    def __str__(self) -> str:
            return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
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