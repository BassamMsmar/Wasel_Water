from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='banners')
    cover = models.ImageField(upload_to='banners')
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    facebook = models.URLField()
    twitter = models.URLField()
    instagram = models.URLField()
    linkedin = models.URLField()
    tiktok = models.URLField()
    whatsapp = models.URLField()

class Banner(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='banners')
    link = models.URLField()
    