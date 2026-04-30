from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from accounts.models import Account
from django.contrib import messages


def RegisterUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please sign in.")
            return redirect('login_user')
        else:
            return render(request, "Authentication/Register.html", {"form": form})
    else:
        form = RegisterForm()
        return render(request, 'Authentication/Register.html', {'form': form})


def LoginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password. Please try again.")
                return render(request, 'Authentication/login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'Authentication/login.html', {'form': form})


def LogoutUser(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')
