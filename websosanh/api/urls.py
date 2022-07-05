
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:pk>/', views.CategoryDetail.as_view()),
    path('categories/<slug:slug>/', views.CategorySlugList.as_view()),
    path('products/search/', views.ProductSearch.as_view()),
    path('products/', views.ProductList.as_view()),
    path('products/detail/<int:pk>/', views.ProductDetail.as_view()),
    path('rawproducts/<int:offset>/<int:limit>/', views.RawProductList.as_view()),
    path('rawcategory/<int:offset>/<int:limit>/', views.RawCategoryList.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)