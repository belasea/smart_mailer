from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import StreamingHttpResponse
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import RegisterForm, LoginForm, UserUpdateForm
from .models import User
from notification.models import Notification
from smart_mailer.local_settings import BASE_URL
  

def register_view(request):
    """
    Handle user registration.
    """
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data['email']
            form.save()
            messages.success(request,"Registration successfully Completed !")
            # Create a notification for the user
            notification_message = f'Created : {email}'
            try:
                # Set the appropriate link if needed
                link = BASE_URL + "user-list"
            except:
                link = None
            notification = Notification(user=request.user, message=notification_message, link=link)
            notification.save()

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
    context = {
        'user_form': user_form,
        'obj': user_obj
    }
    return render(request, 'accounts/profile.html', context)


def user_list(request):
    posts_list = User.objects.all()
    query = request.GET.get('q')
    if query:
        query = query.strip()
        posts_list = posts_list.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(email__icontains=query) |
            Q(contact_number__icontains=query)
        ).distinct()

    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'object_list': posts,
        'page': page,
        'query': query
    }
    return render(request, 'accounts/user_list/user_list.html', context)



# Delete Obj Contact List =============================================
def delete_user(request, id):
    if not request.user.is_superuser:
        messages.warning(request, 'Only superuser can access this.')
        return redirect('home')

    obj = get_object_or_404(User, pk=id)
    context = {'obj': obj}

    if request.method == "POST":
        obj.delete()
        messages.warning(request, 'Successfully deleted this contact.')
        return redirect("user_list")

    return render(request, 'accounts/user_list/delete_user.html', context)



class Echo:
    """An object that implements just the write method of the file-like interface."""
    def write(self, value):
        return value

def export_users_csv(request):
    """Export users as CSV using streaming response."""
    # Define the column headers
    headers = [
        'ID', 'Email', 'First Name', 'Last Name', 'Contact Number',
        'Gender', 'Date of Birth', 'Is Moderator', 'Profile'
    ]

    # Create a generator that yields each row
    def row_generator():
        yield headers
        for user in User.objects.all():
            yield [
                user.id,
                user.email,
                user.first_name,
                user.last_name,
                user.contact_number,
                user.get_gender_display() if user.gender else '',
                user.date_of_birth,
                'Yes' if user.is_moderator else 'No',
                user.profile.url if user.profile else ''
            ]

    # Create a CSV writer that writes to the Echo instance
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)

    # Create a streaming response
    response = StreamingHttpResponse(
        (writer.writerow(row) for row in row_generator()),
        content_type="text/csv"
    )
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    return response
