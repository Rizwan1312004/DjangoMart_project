from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from accounts.models import Account
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required


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


@login_required
def Dashboard(request):
    return render(request, 'Dashboard/dashboard.html')


def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('Authentication/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.content_subtype = 'html'
            send_email.send()
            messages.success(request, "Password reset link sent to your email.")
            return redirect('forgotPassword')
        else:
            messages.error(request, "No account found with this email address.")
    return render(request, 'Authentication/forgotPassword.html')


def ResetPasswordValidate(request, uidb64, token):
    """
    Clicked from the email link.
    Validates uid + token, then redirects to the reset form.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Store uid in session so the confirm view knows which user to update
        request.session['uid'] = uid
        messages.success(request, "Please enter your new password.")
        return redirect('resetpassword_confirm')
    else:
        messages.error(request, "This password reset link is invalid or has expired.")
        return redirect('forgotPassword')


def ResetPassword(request):
    """
    Displays and processes the new-password form.
    """
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('resetpassword_confirm')

        uid = request.session.get('uid')
        if not uid:
            messages.error(request, "Session expired. Please request a new reset link.")
            return redirect('forgotPassword')

        try:
            user = Account.objects.get(pk=uid)
        except Account.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('forgotPassword')

        user.set_password(password)
        user.save()
        # Clear the session uid
        del request.session['uid']
        messages.success(request, "Your password has been reset. Please log in.")
        return redirect('login_user')

    return render(request, 'Authentication/resetPassword.html')