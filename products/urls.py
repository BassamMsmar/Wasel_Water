from django.urls import path
from .views import ProductList, ProductDetail, BrandList, BrandDetail, CategoryList, CategoryDetail, OfferList, OfferDetail


urlpatterns = [
    path('products/', ProductList.as_view(), name='product_list'),
    path('products/<str:slug>', ProductDetail.as_view(), name='product_detail'),

    path('brands/', BrandList.as_view(), name='brand_list'), 
    path('brands/<slug:slug>', BrandDetail.as_view(), name='brand_details'), 

    path('categories/', CategoryList.as_view(), name='category_list'), 
    path('categories/<int:pk>', CategoryDetail.as_view(), name='category_details'), 

    path('offers/', OfferList.as_view(), name='offer_list'), 
    path('offers/<str:slug>', OfferDetail.as_view(), name='offer_detail'), 


]