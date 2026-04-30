from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    path('<slug:category_slug>/', views.StoreView.as_view(), name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('<slug:category_slug>/<slug:product_slug>/submit_review/', views.SubmitReviewView.as_view(), name='submit_review'),
]

    