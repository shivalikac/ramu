from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import PantryItem, UtensilItem
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


# Welcome page view (for non-logged-in users)
def welcome(request):
    return render(request, 'accounts/welcome.html')

@require_POST
@login_required
def delete_pantry_item(request):
    item_id = request.POST.get('item_id')
    item = get_object_or_404(PantryItem, id=item_id, user=request.user)
    item.delete()
    return JsonResponse({"status": "success", "item_id": item_id})

@require_POST
@login_required
def delete_utensil_item(request):
    item_id = request.POST.get('item_id')
    item = get_object_or_404(UtensilItem, id=item_id, user=request.user)
    item.delete()
    return JsonResponse({"status": "success", "item_id": item_id})

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
    
@login_required
def main_welcome(request):
    pantry_items = PantryItem.objects.filter(user=request.user)
    utensil_items = UtensilItem.objects.filter(user=request.user)
    return render(request, 'accounts/main_welcome.html', {
        'pantry_items': pantry_items,
        'utensil_items': utensil_items
    })

@login_required
def add_pantry_item(request):
    if request.method == "POST":
        item_name = request.POST.get("item_name")
        quantity = request.POST.get("quantity", 1)
        PantryItem.objects.create(user=request.user, item_name=item_name, quantity=quantity)
        return JsonResponse({"status": "success", "item": item_name, "quantity": quantity})
    return JsonResponse({"status": "error"}, status=400)

@login_required
def add_utensil_item(request):
    if request.method == "POST":
        utensil_name = request.POST.get("utensil_name")
        quantity = request.POST.get("quantity", 1)
        UtensilItem.objects.create(user=request.user, utensil_name=utensil_name, quantity=quantity)
        return JsonResponse({"status": "success", "utensil": utensil_name, "quantity": quantity})
    return JsonResponse({"status": "error"}, status=400)

# Register View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_welcome')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('main_welcome')

def custom_logout(request):
    logout(request)  # Log the user out
    return redirect('welcome')  # Redirect to the welcome page (or any page you prefer)
