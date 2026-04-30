from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add/', views.AddCartView.as_view(), name='add_cart'),
    path('add/ajax/', views.AddCartAjaxView.as_view(), name='add_cart_ajax'),
    path('remove/<str:slug>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('increment/<str:slug>/', views.IncrementCartView.as_view(), name='increment_cart'),
    path('decrement/<str:slug>/', views.DecrementCartView.as_view(), name='decrement_cart'),
]
