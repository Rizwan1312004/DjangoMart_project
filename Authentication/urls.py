from django.urls import path
from . import views

urlpatterns = [
    path("register", views.RegisterUser, name="register_user"),
    path("login", views.LoginUser, name="login_user"),
    path("logout", views.LogoutUser, name="logout_user"),
    path('dashboard', views.Dashboard, name='dashboard'),
    path('forgotPassword', views.ForgotPassword, name='forgotPassword'),
    path('resetpassword/<uidb64>/<token>/', views.ResetPasswordValidate, name='resetpassword_validate'),
    path('resetpassword/confirm/', views.ResetPassword, name='resetpassword_confirm'),
]