from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def store(request, category_slug=None):
    categories = Category.objects.all() 
    products = None

    if category_slug is not None:
        current_category = get_object_or_404(Category, cat_slug=category_slug)
        products = Product.objects.filter(category=current_category, is_available=True).order_by('created_date')
        product_count = products.count()
        
    else:
        products = Product.objects.filter(is_available=True).order_by('created_date')
        product_count = products.count()

    context = {
        'products': products,
        'categories': categories, 
        'product_count': product_count,
    }
    
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    product = Product.objects.get(category__cat_slug=category_slug, slug=product_slug)
    try:
        single_product = Product.objects.get(category__cat_slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    context = {
        'single_product': single_product,
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)