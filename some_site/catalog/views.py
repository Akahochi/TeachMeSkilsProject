from typing import Any, Optional
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Prefetch
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from cart.forms import CartAddProductForm
from catalog.models import Category, Product


# def home(request):
#     cat = Category.objects.all()
#     return render(
#         request,
#         'catalog/home.html',
#         {"categories": cat}
#     )

# class HomeView(View):
#     def get(self, request):
#         cat = Category.objects.all()
#         return render(
#             request,
#             'catalog/home.html',
#             {"categories": cat}
#         )


# class HomeTemplateView(LoginRequiredMixin, TemplateView):
#     template_name = 'catalog/home.html'
#
#     def get_context_data(self, **kwargs):
#         context: dict[str, Any] = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.annotate(Count('products'))
#         return context
#
# @login_required(login_url=reverse_lazy('authentification:login')) """Либо скопировать это в нстройки"""
# Тогда без урла можно использовать декаратор (по сути мы поменяли его значение по умолчанию в настройках)
# @login_required
# def category(request: WSGIRequest, categoty_slug: str):
#     try:
#         category: Category = (
#             Category.objects
#             .prefetch_related('products')
#             .get(slug=categoty_slug)
#         )
#     except Category.DoesNotExist:
#         raise Http404
#     return render(request, 'catalog/product.html', {'category': category})

class HomeViev(View):

    def get(self, request):
        category = Category.objects.order_by('name')
        return render(request, 'catalog/home.html', {'category': category})


#
# def category_view(request, category_slug):
#     products = Product.objects.filter(category__slug=category_slug).order_by('name')
#     return render(request, 'catalog/product.html', {'products': products})


# def category_view(request, category_slug):
#     products = Product.objects.filter(category__slug=category_slug).order_by('name')
#     cart_product_form = CartAddProductForm()
#     return render(request, 'catalog/product.html', {'products': products, 'cart_product_form': cart_product_form})


def category_view(request, category_slug):
    products = Product.objects.filter(category__slug=category_slug).order_by('name')
    cart_product_form = CartAddProductForm()
    paginator = Paginator(products, 2)  # 2 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'catalog/product.html',
                  {'products': products, 'cart_product_form': cart_product_form, 'page': page, 'posts': posts})


class ProductView(View):

    def get(self, request, product_slug):
        product = Product.objects.filter(slug=product_slug).first()
        cart_product_form = CartAddProductForm()
        return render(request, 'catalog/description.html', {'product': product, 'cart_product_form': cart_product_form})

# def product(request:WSGIRequest, category_slug, product_slug):
#
#     product: Optional[Product] = (
#         Product.objects
#         .prefetch_related('modifier_groups')
#         .prefetch_related('modifier_groups__modifier_set')
#         .prefetch_related('productimage_set')
#         .filter(slug=product_slug)
#         .first()
#     )
#     if not product:
#         raise Http404
#     return render(request, 'catalog/product.html', {'product': product})
