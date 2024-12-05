import json
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
import requests
from .model_utils import get_recipes_from_spoonacular
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import CalendarEvent
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def recipe_notes(request, event_id):
    event = get_object_or_404(CalendarEvent, id=event_id, user=request.user)

    if request.method == "POST":
        data = json.loads(request.body)
        notes = data.get('notes', '').strip()
        event.notes = notes
        event.save()
        return JsonResponse({"status": "success", "message": "Notes updated successfully."})

    # Render the recipe notes page
    return render(request, 'accounts/recipe_notes.html', {
        "title": event.title,
        "recipe_url": event.recipe_url,  # Ensure the URL is passed here
        "notes": event.notes,
        "event_id": event.id,
        'date': event.date,  # Pass the date to the template
        'meal_type': event.meal_type  # Pass the meal type to the template
    })

@login_required
def add_grocery_shopping_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        date = data.get('date')

        if not date:
            return JsonResponse({"status": "error", "message": "Date is required."}, status=400)

        try:
            CalendarEvent.objects.create(
                user=request.user,
                title="Grocery Shopping!",
                date=date,
                meal_type=None,  # Explicitly set to None for grocery shopping
                image=None,
                recipe_id=None,
                recipe_url=None  # No recipe link for grocery shopping
            )
            return JsonResponse({"status": "success", "message": "Grocery shopping event added successfully."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)


@login_required
def grocery_notes(request, event_id):
    event = get_object_or_404(CalendarEvent, id=event_id, user=request.user)

    if request.method == "POST":
        data = json.loads(request.body)
        notes = data.get('notes', '').strip()
        event.notes = notes
        event.save()
        return JsonResponse({"status": "success", "message": "Notes updated successfully."})

    # Render the grocery notes page
    return render(request, 'accounts/grocery_notes.html', {
        "title": event.title,
        "notes": event.notes,
        "event_id": event.id,
        'date': event.date  # Pass the date to the template
    })

# Welcome page view (for non-logged-in users)
def welcome(request):
    return render(request, 'accounts/welcome.html')

@require_POST
@login_required
def delete_pantry_item(request):
    if request.method == "POST":
        data = json.loads(request.body)
        item_id = data.get('item_id')

        if not item_id:
            return JsonResponse({"status": "error", "message": "Item ID is required."}, status=400)

        try:
            item = PantryItem.objects.get(id=item_id, user=request.user)
            item.delete()
            return JsonResponse({"status": "success", "message": "Item deleted successfully."})
        except PantryItem.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Item not found."}, status=404)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)


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
        data = json.loads(request.body)
        item_name = data.get('item_name')
        quantity = data.get('quantity')

        if not item_name or not quantity:
            return JsonResponse({"status": "error", "message": "Both item name and quantity are required."}, status=400)

        try:
            # Create a new pantry item
            new_item = PantryItem.objects.create(
                user=request.user,
                item_name=item_name,
                quantity=quantity
            )
            return JsonResponse({"status": "success", "item_id": new_item.id, "item": item_name, "quantity": quantity})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

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

@login_required
def fetch_calendar_events(request):
    events = CalendarEvent.objects.filter(user=request.user)
    event_list = [
        {
            "title": event.title,
            "start": event.date.isoformat(),
            "image": event.image,  # Optional, if needed
        }
        for event in events
    ]
    return JsonResponse(event_list, safe=False)

@login_required
def add_to_calendar(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get('title')
        image = data.get('image')
        recipe_id = data.get('recipe_id')
        date = data.get('date')
        meal_type = data.get('meal_type')

        if not (title and date and meal_type):
            return JsonResponse({"status": "error", "message": "Title, date, and meal type are required."}, status=400)

        try:
            # Generate the Spoonacular recipe URL if a recipe_id is provided
            recipe_url = f"https://spoonacular.com/recipes/{title.replace(' ', '-')}-{recipe_id}" if recipe_id else None

            # Add the event to the calendar
            CalendarEvent.objects.create(
                user=request.user,
                title=title,
                image=image,
                recipe_id=recipe_id,
                recipe_url=recipe_url,  # Save the recipe URL
                date=date,
                meal_type=meal_type
            )
            return JsonResponse({"status": "success", "message": "Event added to calendar successfully."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)


@login_required
def generate_recipe(request):
    if request.method == "POST":
        data = json.loads(request.body)
        recipe_count = data.get('recipe_count', 5)
        cuisine = data.get('cuisine', None)
        cooking_time = data.get('cooking_time', None)
        intolerances = data.get('intolerances', [])

        pantry_items = list(PantryItem.objects.filter(user=request.user).values_list('item_name', flat=True))

        # Prepare API request parameters
        params = {
            "ingredients": ",".join(pantry_items),
            "number": recipe_count,
            "cuisine": cuisine if cuisine else None,
            "maxReadyTime": cooking_time if cooking_time else None,
            "intolerances": ",".join(intolerances) if intolerances else None,  # Add intolerances
            "apiKey": settings.SPOONACULAR_API_KEY
        }

        # Make API request to Spoonacular
        response = requests.get("https://api.spoonacular.com/recipes/findByIngredients", params=params)

        if response.status_code == 200:
            recipes = response.json()
            return JsonResponse({"recipes": recipes})
        else:
            return JsonResponse({"error": "Failed to fetch recipes."}, status=response.status_code)

    return JsonResponse({"error": "Invalid request method."}, status=400)

@login_required
def schedule(request):
    return render(request, 'accounts/schedule.html')
    
def link_calendar(request, calendar_type):
    if calendar_type == "google":
        oauth_url = "https://accounts.google.com/o/oauth2/auth"
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "https://www.googleapis.com/auth/calendar.readonly",
            "access_type": "offline",
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return HttpResponseRedirect(f"{oauth_url}?{query_string}")

    elif calendar_type == "microsoft":
        oauth_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
        params = {
            "client_id": settings.MICROSOFT_CLIENT_ID,
            "redirect_uri": settings.MICROSOFT_REDIRECT_URI,
            "response_type": "code",
            "scope": "Calendars.Read",
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return HttpResponseRedirect(f"{oauth_url}?{query_string}")

    return HttpResponseRedirect('/schedule/')

def oauth_callback(request, calendar_type):
    code = request.GET.get('code')
    if calendar_type == "google":
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
    elif calendar_type == "microsoft":
        token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        data = {
            "code": code,
            "client_id": settings.MICROSOFT_CLIENT_ID,
            "client_secret": settings.MICROSOFT_CLIENT_SECRET,
            "redirect_uri": settings.MICROSOFT_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
    else:
        return HttpResponseRedirect('/schedule/')

    # Request access token
    response = requests.post(token_url, data=data)
    tokens = response.json()
    # Store tokens in the session or database for authenticated user
    request.session[f"{calendar_type}_tokens"] = tokens
    return HttpResponseRedirect('/schedule/')

@login_required
def fetch_calendar_events(request):
    events = CalendarEvent.objects.filter(user=request.user)
    event_list = [
        {
            "id": event.id,
            "title": event.title,
            "start": event.date.isoformat(),
            "meal_type": event.meal_type,
            "image": event.image,
            # "recipe_url": f"https://spoonacular.com/recipes/{event.title.replace(' ', '-')}-{event.recipe_id}" if event.recipe_id else None
            "recipe_url": event.recipe_url,  # Optional if you still want to show this
        }
        for event in events
    ]

    # Debug: Print the event list
    print("Events sent to FullCalendar:", event_list)

    return JsonResponse(event_list, safe=False)


@login_required
def delete_calendar_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        event_id = data.get('event_id')

        # Validate event_id
        if not event_id:
            return JsonResponse({"status": "error", "message": "Event ID is required."}, status=400)

        try:
            # Ensure event_id is an integer
            event = CalendarEvent.objects.get(id=int(event_id), user=request.user)
            event.delete()
            return JsonResponse({"status": "success", "message": "Event deleted successfully."})
        except ValueError:
            return JsonResponse({"status": "error", "message": "Invalid event ID."}, status=400)
        except CalendarEvent.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Event not found."}, status=404)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)


@login_required
def add_manual_calendar_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get('title')
        date = data.get('date')
        meal_type = data.get('meal_type')

        if not (title and date and meal_type):
            return JsonResponse({"status": "error", "message": "Title, date, and meal type are required."}, status=400)

        CalendarEvent.objects.create(
            user=request.user,
            title=title,
            date=date,
            meal_type=meal_type
        )

        return JsonResponse({"status": "success", "message": "Event added successfully."})

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)
