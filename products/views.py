from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count, Q
from django.db.models.aggregates import Avg
# from .tasks import send_emails
from .models import Product, Brand, Review, ProductImages, Category, Offer
# Create your views here.
from django.http import JsonResponse
from django.template.loader import render_to_string


class ProductList(ListView):
    model = Product
    queryset = Product.objects.filter(product_type='single')    
    paginate_by = 20
    



class ProductDetail(DetailView):
    model =Product
    queryset = Product.objects.all()



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(product=self.get_object())
        context["related_products"] = Product.objects.filter(brand=self.get_object().brand) 
        return context
    

class BrandList(ListView):
    model = Brand    #context : object_list, model_list
    paginate_by = 20
    queryset = Brand.objects.all()
 

class BrandDetail(ListView):
    model = Product     #context : object_list, model_list
    template_name = 'product/brand_detail.html'


    def get_queryset(self):
        brand = Brand.objects.get(slug=self.kwargs['slug'])
        return super().get_queryset().filter(brand=brand) 
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brand"] = Brand.objects.get(slug=self.kwargs['slug'])


class CategoryList(ListView):
    model = Category
    paginate_by = 20
    queryset = Category.objects.all()


class CategoryDetail(ListView):
    model = Product     #context : object_list, model_list
    template_name = 'product/category_detail.html'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return super().get_queryset().filter(categories=category) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(slug=self.kwargs['slug'])


class OfferList(ListView):
    model = Offer
    queryset = Offer.objects.all()
    paginate_by = 20


class OfferDetail(DetailView):
    model = Offer
    queryset = Offer.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["offer"] = Offer.objects.get(slug=self.kwargs['slug'])
        return context

