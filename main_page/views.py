from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

from main_page.models import Category, Product
from cart.forms import CartAddProductForm
from main_page.recommender import Recommender


def home(request):
    return render(request, 'main_page/homepage.html')


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                     translations__language_code=language,
                                     translations__slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'main_page/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                translations__language_code=language,
                                id=id,
                                translations__slug=slug,
                                available=True)
    cart_product_from = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request,
                  'main_page/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_from,
                   'recommended_products': recommended_products
                   })
