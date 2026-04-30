from store.models import Product
from category.models import Category
from django.shortcuts import render

def home(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    cart_items = request.session.get('cart', {})
    
    context = {
        'products': products,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'home.html', context)

def search_product(request):
    cart_items = request.session.get('cart', {})
    
    if request.method == 'GET':
        product_name = request.GET.get('q', '')
        if product_name:
            products = Product.objects.filter(product_name__icontains=product_name)
        else:
            products = Product.objects.all()
        return render(request, 'store/store.html', {'products': products, 'search_query': product_name, 'cart_items': cart_items})