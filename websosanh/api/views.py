from itertools import product
from multiprocessing import context
from typing import Set
from unicodedata import category
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import status
from .models import Category, Product, RawCategory, RawProduct
from .serializers import ProductSerializer, RawProductSerializer, UserSerializer, GroupSerializer, CategorySerializer, RawCategorySerializer
from django.http import Http404
from django.http import HttpRequest
from .query import query as q


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategorySlugList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class CategoryDetail(APIView):

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductList(APIView):
    def get(self, request,format=None, **kwargs):
        catid = kwargs.get('catid')
        products = Product.objects.all().select_related().filter(category=catid)
        
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        from django.db import connection, transaction
        cursor = connection.cursor()

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            price = serializer.data.get('price')
            url = serializer.data.get('url')
            imageLink = serializer.data.get('imageLink')
            category_id = serializer.initial_data.get('category')
            query = q.insertProduct(name, price, url, imageLink, category_id)
            cursor.execute(query)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RawProductList(APIView):
    def get(self, request, format=None, *args, **kwargs):
        limit = kwargs.get('limit')
        offset = kwargs.get('offset')
        products = RawProduct.objects.all().order_by('id')[offset:offset+limit].select_related('subcategory')
        serializer = RawProductSerializer(products, many=True)

        return Response(serializer.data)

class RawCategoryList(APIView):
    def get(self, request, format = None, *arg, **kwargs):
        limit = kwargs.get('limit')
        offset = kwargs.get('offset')
        category = RawCategory.objects.all().order_by('id')[offset:offset+limit]
        serializer = RawCategorySerializer(category,many = True)
        return Response(serializer.data)
