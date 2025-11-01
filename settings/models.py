from django.db import models

# Create your models here.


class Banner(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='banners')
    link = models.URLField()
    