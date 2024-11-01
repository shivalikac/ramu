from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.models import User

# Welcome page view (for non-logged-in users)
def welcome(request):
    return render(request, 'accounts/welcome.html')

@login_required
def profile(request):
    users = None
    # Check if the logged-in user is a superuser
    if request.user.is_superuser:
        users = User.objects.all()  # Get all users if the user is a superuser

    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'all_users': users  # Pass the list of users to the template
    })
    
# Main Welcome Page View
@login_required
def login_welcome(request):
    return render(request, 'accounts/login_welcome.html')

# Register View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_welcome')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('login_welcome')

def custom_logout(request):
    logout(request)  # Log the user out
    return redirect('welcome')  # Redirect to the welcome page (or any page you prefer)
