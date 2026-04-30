# DjangoMart Project Interview Questions

Based on a detailed analysis of the **DjangoMart** codebase, here are the most important technical interview questions an engineering manager or technical lead might ask. These questions are tailored to the specific architectural, design, and implementation choices made in this project.

## 1. Custom User Authentication Models
**Context:** The project uses a custom `Account` model that inherits from `AbstractBaseUser` instead of Django's default `User` or `AbstractUser`. It also implements a custom `MyAccountManager`.

* **Question:** "In this project, the `Account` model inherits from `AbstractBaseUser` and sets `USERNAME_FIELD = 'email'`. Can you explain the difference between `AbstractBaseUser` and `AbstractUser`? Why did you choose this approach, and how does the custom `MyAccountManager` handle user and superuser creation?"
* **What the interviewer is looking for:** Understanding of Django's auth system flexibility, the necessity of overriding the base manager when changing the `USERNAME_FIELD`, and the difference between just adding fields (`AbstractUser`) vs rebuilding the authentication logic (`AbstractBaseUser`).

## 2. Session-Based Shopping Cart Management
**Context:** The `carts` app doesn't define any database models (e.g., no `Cart` or `CartItem` models). Instead, cart items, quantities, and totals are stored and manipulated entirely within `request.session`.

* **Question:** "You chose to implement the shopping cart using Django's session framework rather than storing cart items in a database table. What are the performance and scalability advantages of this approach? Conversely, how would you handle cart persistence if a user logs in from a different device, given that sessions are device/browser specific?"
* **What the interviewer is looking for:** Knowledge of server-side sessions, avoiding unnecessary database I/O for anonymous users, and awareness of the limitations of session-based carts (cart abandonment across devices) and how to migrate session data to a database model upon authentication.

## 3. Database Aggregation vs. Python-level Processing
**Context:** In the `StoreView`, you use Django's ORM to annotate the queryset with an average rating: `products.annotate(raw_avg=Avg('reviewrating__rating'))`. However, immediately afterward, you loop through the queryset in Python to round the `avg_rating` for each product.

* **Question:** "In your store view, you annotate the product queryset with the average rating from the database, but then iterate over the evaluated queryset in a `for p in products:` loop to round the rating. What are the performance implications of evaluating the queryset and modifying objects in Python memory? How could you push this rounding logic down to the database level using Django ORM functions like `Round` or `Cast`?"
* **What the interviewer is looking for:** Understanding of ORM lazy evaluation, the N+1 query problem (though not strictly applicable here, the concept of DB vs App memory is), and knowledge of advanced Django database functions.

## 4. Queryset Sorting in Memory
**Context:** In `StoreView`, when the user requests a specific sort order (e.g., 'low-to-high'), the code evaluates the queryset and sorts it using Python's built-in `sorted()` function: `sorted(products, key=lambda p: p.price)`.

* **Question:** "I noticed that product sorting is handled using Python's `sorted()` function on the evaluated queryset rather than using the ORM's `.order_by('price')`. Why was this approach taken? What would happen to your application's memory usage and response time if the product catalog grew to 100,000 items?"
* **What the interviewer is looking for:** Awareness of database-level sorting efficiency vs. application-level sorting. The interviewer expects you to recognize that sorting in Python forces the entire table into RAM, whereas `.order_by()` uses the database engine's optimized sorting (and indexes).

## 5. Asynchronous Operations (AJAX) & CSRF
**Context:** The `AddCartAjaxView` is designed to add products to the session cart without triggering a full page reload, returning a `JsonResponse` instead of a redirect.

* **Question:** "Your project includes an `AddCartAjaxView` that accepts POST requests to update the cart asynchronously. How did you handle CSRF protection for these JavaScript fetch/XHR requests? Explain the flow of data between the frontend script and this specific Django view."
* **What the interviewer is looking for:** Understanding of how Django's CSRF middleware works, how to extract the CSRF token from cookies or DOM meta tags in JavaScript, and the anatomy of a JSON response.

## 6. Class-Based Views (CBVs) & Mixins
**Context:** The project heavily utilizes Django's Class-Based Views (`View`, `TemplateView`) and Mixins (`LoginRequiredMixin`).

* **Question:** "The `SubmitReviewView` inherits from both `LoginRequiredMixin` and `View`. Can you explain how Python's Method Resolution Order (MRO) applies here, and why it's critical that `LoginRequiredMixin` is listed first in the inheritance declaration? Why choose CBVs over function-based views for this project?"
* **What the interviewer is looking for:** Solid understanding of Object-Oriented Python, multiple inheritance, Django view lifecycle (dispatch method), and the reusability benefits of CBVs.

## 7. E-commerce Financial Calculations
**Context:** The `CartView` computes `subtotal`, `tax`, and `grand_total` dynamically in the `get_context_data` method based on session data.

* **Question:** "You are currently calculating taxes and grand totals dynamically in the view on every request. In a production environment where tax rates might change historically or differ by region, how would you refactor this to ensure that past order totals remain immutable?"
* **What the interviewer is looking for:** Architecture skills related to decoupling cart logic from order history logic. The expectation is an understanding that an `Order` model must snapshot prices, taxes, and totals at the time of checkout, rather than calculating them dynamically.
