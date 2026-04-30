from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import JsonResponse
from store.models import Product

class CartView(TemplateView):
    """Displays the cart page with quantities and totals computed server-side."""
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Session cart: {slug: quantity}
        session_cart = self.request.session.get('cart', {})

        # Fetch all products that are in the cart
        products = Product.objects.filter(slug__in=session_cart.keys())

        # Build enriched cart items list
        cart_items = []
        subtotal = 0

        for product in products:
            quantity = session_cart.get(product.slug, 1)
            item_total = product.price * quantity
            subtotal += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            })

        # Compute summary figures
        shipping = 10 if subtotal > 0 else 0
        tax = round(subtotal * 0.08, 2)
        grand_total = subtotal + shipping + tax

        context['cart_items'] = cart_items
        context['subtotal'] = subtotal
        context['shipping'] = shipping
        context['tax'] = tax
        context['grand_total'] = grand_total

        return context


class AddCartView(View):
    """Adds a product to the cart and refreshes the page."""
    
    # By naming this 'post', Django knows to ONLY allow POST requests here!
    def post(self, request, *args, **kwargs):
        slug = request.POST.get('slug')
        product = get_object_or_404(Product, slug=slug)
        
        cart = request.session.get('cart', {})
        cart[slug] = cart.get(slug, 0) + 1
            
        request.session['cart'] = cart
        request.session.modified = True
        
        messages.success(request, f"{product.product_name} added to cart.")
        return redirect('store')


class AddCartAjaxView(View):
    """Adds a product to the cart quietly in the background (no refresh)."""
    
    def post(self, request, *args, **kwargs):
        slug = request.POST.get('slug')
        product = get_object_or_404(Product, slug=slug)

        cart = request.session.get('cart', {})
        cart[slug] = cart.get(slug, 0) + 1

        request.session['cart'] = cart
        request.session.modified = True

        return JsonResponse({
            'success': True,
            'message': f"{product.product_name} added to cart!",
            'cart_total': sum(cart.values()),   # total units across all items
            'cart_count': len(cart),             # unique items — matches {{cart_items|length}}
            'slug': slug,
        })


class RemoveFromCartView(View):
    """Removes a product from the cart entirely."""

    def get(self, request, slug, *args, **kwargs):
        cart = request.session.get('cart', {})

        if slug in cart:
            del cart[slug]

            request.session['cart'] = cart
            request.session.modified = True

        return redirect('cart')


class IncrementCartView(View):
    """Adds one more unit of a product already in the cart."""

    def get(self, request, slug, *args, **kwargs):
        cart = request.session.get('cart', {})
        cart[slug] = cart.get(slug, 0) + 1
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart')


class DecrementCartView(View):
    """Removes one unit of a product from the cart; deletes item if quantity reaches 0."""

    def get(self, request, slug, *args, **kwargs):
        cart = request.session.get('cart', {})

        if slug in cart:
            cart[slug] -= 1
            if cart[slug] <= 0:
                del cart[slug]
            request.session['cart'] = cart
            request.session.modified = True

        return redirect('cart')