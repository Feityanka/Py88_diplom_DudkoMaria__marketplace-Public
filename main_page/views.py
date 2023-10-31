from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from main_page.models import Category, Product, Rating, Review
from main_page.forms import RatingForm, ReviewForm
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
    reviews = product.reviews.all()
    ratings = product.ratings.all()
    average_rating = ratings.aggregate(models.Avg('value'))['value__avg']
    if average_rating:
        average_rating = round(average_rating, 1)
    review_form = ReviewForm()
    rating_form = RatingForm()
    cart_product_from = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request,
                  'main_page/product/detail.html',
                  {'product': product,
                   'reviews': reviews,
                   'ratings': ratings,
                   'average_rating': average_rating,
                   'review_form': review_form,
                   'rating_form': rating_form,
                   'cart_product_form': cart_product_from,
                   'recommended_products': recommended_products
                   })


@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('item_detail', pk=product.pk)
    else:
        form = ReviewForm()
    return render(request,
                  'main_page/product/adding_review.html',
                  {
                      'form': form
                  })


@login_required
def add_rating(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.product = product
            rating.user = request.user
            rating.save()
            return redirect('item_detail', pk=product.pk)
    else:
        form = RatingForm()
    return render(request,
                  'main_page/product/adding_rating.html', {
                      'form': form
                  })
