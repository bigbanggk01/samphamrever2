from dataclasses import Field, field
from itertools import product
from operator import sub
from pickletools import read_floatnl
from pyexpat import model
from statistics import mode
from unicodedata import category, name
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Category, Product, RawProduct, RawCategory, SubCategory
from django.forms.models import model_to_dict

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 
                'name', 
                'price', 
                'url', 
                'imageLink', 
                'website', 
                'vote',  
                'slug'
                ]
class RawProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawProduct
        fields = ['id',
        'name',
        'url',
        'imageUrl',
        'price',
        'subcategory'
        ]

class SubCategorySerializer(serializers.ModelSerializer):
    product = RawProductSerializer(many=True, read_only = True)
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'link', 'product']

class RawCategorySerializer(serializers.ModelSerializer):
    #subcategory = SubCategorySerializer(many=True, read_only = True)
    
    class Meta:
        model = RawCategory
        fields = ['id',
        'name',
        'link',
        'siteId'
        ]