from os import link
from unicodedata import category, name
from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique= True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.TextField(max_length=200)
    price = models.CharField(max_length=32)
    url = models.TextField()
    imageLink = models.TextField()
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    slug = models.SlugField(null=True, blank=True, unique=True)
    website = models.CharField(max_length=32, null=False)
    vote = models.SmallIntegerField(null=True)
    vector_column = SearchVectorField(null=True)
    def __str__(self):
        return self.product_name

    class Meta:
        indexes = (GinIndex(fields=["vector_column"]),)

class Site(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 32)
    url = models.CharField(max_length = 32)

class RawCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=400)
    siteId = models.ForeignKey(Site, on_delete= models.CASCADE)

    class Meta:
        ordering = ['name']

class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    link = models.CharField(max_length=400)
    category = models.ForeignKey(RawCategory, related_name='subcategory', on_delete=models.CASCADE)
    
class RawProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    price = models.CharField(max_length=32)
    url = models.CharField(max_length=1000)
    imageUrl = models.TextField(max_length=1000)
    subcategory = models.ForeignKey(SubCategory, related_name='product',on_delete= models.CASCADE, default=1)
    mycategory = models.ForeignKey(Category, on_delete=models.CASCADE, default= 1)