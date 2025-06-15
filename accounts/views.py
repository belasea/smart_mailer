from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm, UserUpdateForm
from .models import User


def register_view(request):
    """
    Handle user registration.
    """
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                "Registration successful! Please check your email to activate your account."
            )
            return redirect('login')
        else:
            messages.error(request, "There was an error in the registration form.")
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Handle user login.
    """
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Logged in as {email}.")
                    return redirect('home')
                else:
                    messages.warning(request, "Account is inactive. Check your email for activation.")
            else:
                messages.error(request, "Invalid email or password.")
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


# def user_profile(request, id): 
#     obj = get_object_or_404(User, pk=id)
    
#     # Optional: Prevent users from editing others' profiles
#     if request.user != obj:
#         messages.error(request, "You are not authorized to edit this profile.")
#         return redirect('home')  # or another safe page

#     if request.method == 'POST':
#         form = UserUpdateForm(request.POST or request.File, instance=obj, )
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your profile was updated successfully.')
#             return redirect('user_profile', id=obj.id)
#     else:
#         form = UserUpdateForm(instance=obj)

#     return render(request, 'accounts/profile.html', {'form': form, 'obj': obj})


def user_profile(request, id):
    user_obj = get_object_or_404(User, pk=id)

    if request.user != user_obj:
        messages.error(request, "You are not authorized to edit this profile.")
        return redirect('home')

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user_obj)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile was updated successfully.')
            return redirect('user_profile', id=user_obj.id)
    else:
        user_form = UserUpdateForm(instance=user_obj)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'obj': user_obj
    })
