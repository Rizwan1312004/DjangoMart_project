from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages 
from .models import Product, Category, ReviewRating
from .forms import ReviewForm 
from django.db.models import Avg

class StoreView(View):
    """Displays the main store page and handles category filtering."""
    
    def get(self, request, category_slug=None, *args, **kwargs):
        # 1. Grab things we need no matter what
        categories = Category.objects.all()
        cart_items = request.session.get('cart', {})

        
        # 2. Check if the user is looking at a specific category
        if category_slug:
            current_category = get_object_or_404(Category, cat_slug=category_slug)
            products = Product.objects.filter(category=current_category, is_available=True).order_by('created_date')
        else:
            # Otherwise, show all available products
            products = Product.objects.filter(is_available=True).order_by('created_date')

        # 3. Package everything up and send it to the template
        products = products.annotate(raw_avg=Avg('reviewrating__rating'))
       
        for p in products:
            if p.raw_avg is not None:
               p.avg_rating = round(p.raw_avg * 2) / 2
            else:
                p.avg_rating = 0.0
        
        sort = request.GET.get('sort', 'newest')
        if sort == 'low-to-high':
            products = sorted(products, key=lambda p: p.price)
        elif sort == 'high-to-low':
            products = sorted(products, key=lambda p: p.price, reverse=True)
        elif sort == 'popular':
            products = sorted(products, key=lambda p: p.stock, reverse=True)
        else:  # newest (default)
            sort = 'newest'
            products = sorted(products, key=lambda p: p.created_date, reverse=True)


        context = {
            'products': products,
            'categories': categories, 
            'product_count': len(products), 
            'cart_items': cart_items,
            'sort': sort,
        }
        
        return render(request, 'store/store.html', context)


class ProductDetailView(View):
    """Displays the details for a single product."""
    
    def get(self, request, category_slug, product_slug, *args, **kwargs):
        # Safely get the product, or return a 404 Page Not Found if it doesn't exist
        product = get_object_or_404(Product, category__cat_slug=category_slug, slug=product_slug)
        cart_items = request.session.get('cart', {})
        # Note: Depending on your model fields, you might need 'created_at' or 'created_date'
        reviews = ReviewRating.objects.filter(product=product).order_by('-created_date') 
        avgRating = ReviewRating.objects.filter(product=product).aggregate(rating__avg=Avg('rating'))

        raw_avg = avgRating['rating__avg']

        if raw_avg is not None:
            avgRating['rating__avg'] = round(raw_avg * 2) / 2
        else:
            avgRating['rating__avg'] = 0.0            
        context = {
            'product': product,
            'cart_items': cart_items,
            'reviews': reviews,
            'avgRating': avgRating,
        }
        
        return render(request, 'store/product_detail.html', context)

class SubmitReviewView(LoginRequiredMixin, View):
    """Handles the submission of product reviews using a ModelForm."""
    login_url = '/'  # No dedicated login page; redirect home if not authenticated
    
    def post(self, request, category_slug, product_slug, *args, **kwargs):
        product = get_object_or_404(Product, category__cat_slug=category_slug, slug=product_slug)

        # Always create a new comment so multiple reviews can stack up
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            if not review.subject:
                review.subject = f"Review by {request.user.username}"
            review.save()
            messages.success(request, 'Thank you! Your comment has been posted.')
        else:
            messages.error(request, 'There was a problem posting your comment. Please try again.')

        return redirect('product_detail', category_slug=category_slug, product_slug=product_slug)
    
