import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from .models import PantryItem, UtensilItem, CalendarEvent
import requests

@login_required
def recipe_notes(request, event_id):
    """
    Handle recipe notes for a specific calendar event.

    GET: Renders the recipe notes page with event details.
    POST: Updates the notes for the given calendar event.

    Args:
        request: The HTTP request object.
        event_id: The ID of the calendar event.

    Returns:
        JsonResponse on successful update or rendered HTML for GET requests.
    """
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
        "recipe_url": event.recipe_url,
        "notes": event.notes,
        "event_id": event.id,
        'date': event.date,
        'meal_type': event.meal_type
    })


@login_required
def add_grocery_shopping_event(request):
    """
    Add a grocery shopping event to the user's calendar.

    POST: Creates a new grocery shopping calendar event.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse indicating success or error.
    """
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
                meal_type=None,
                image=None,
                recipe_id=None,
                recipe_url=None
            )
            return JsonResponse({"status": "success", "message": "Grocery shopping event added successfully."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)


@login_required
def grocery_notes(request, event_id):
    """
    Handle grocery notes for a specific calendar event.

    GET: Renders the grocery notes page with event details.
    POST: Updates the notes for the given calendar event.

    Args:
        request: The HTTP request object.
        event_id: The ID of the calendar event.

    Returns:
        JsonResponse on successful update or rendered HTML for GET requests.
    """
    event = get_object_or_404(CalendarEvent, id=event_id, user=request.user)

    if request.method == "POST":
        data = json.loads(request.body)
        notes = data.get('notes', '').strip()
        event.notes = notes
        event.save()
        return JsonResponse({"status": "success", "message": "Notes updated successfully."})

    return render(request, 'accounts/grocery_notes.html', {
        "title": event.title,
        "notes": event.notes,
        "event_id": event.id,
        'date': event.date
    })


def welcome(request):
    """
    Render the welcome page for non-logged-in users.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered HTML page for the welcome view.
    """
    return render(request, 'accounts/welcome.html')


@require_POST
@login_required
def delete_pantry_item(request):
    """
    Delete a pantry item for the logged-in user.

    POST: Deletes the specified pantry item.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse indicating success or error.
    """
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


@login_required
def delete_utensil_item(request):
    """
    Delete a utensil item for the logged-in user.

    POST: Deletes the specified utensil item.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse indicating success or error.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            utensil_id = data.get('item_id')
            if not utensil_id:
                return JsonResponse({'status': 'error', 'message': 'Item ID is missing.'}, status=400)

            utensil_item = UtensilItem.objects.get(id=utensil_id, user=request.user)
            utensil_item.delete()
            return JsonResponse({'status': 'success', 'message': 'Utensil deleted successfully.'})
        except UtensilItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Utensil not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


@login_required
def profile(request):
    """
    Display the user's profile page.

    If the user is a superuser, display a list of all users.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered HTML page for the profile view.
    """
    users = User.objects.all() if request.user.is_superuser else None

    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'all_users': users
    })


@login_required
def main_welcome(request):
    """
    Display the main welcome page with the user's pantry and utensil items.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered HTML page for the main welcome view.
    """
    pantry_items = PantryItem.objects.filter(user=request.user)
    utensil_items = UtensilItem.objects.filter(user=request.user)
    return render(request, 'accounts/main_welcome.html', {
        'pantry_items': pantry_items,
        'utensil_items': utensil_items
    })

@login_required
def add_pantry_item(request):
    """
    Add a new pantry item for the logged-in user.

    POST: Adds a new pantry item with the specified name and quantity.

    Args:
        request: The HTTP request object containing JSON data with 'item_name' and 'quantity'.

    Returns:
        JsonResponse: A success message with the created item's details or an error message.
    """
    if request.method == "POST":
        data = json.loads(request.body) 
        item_name = data.get('item_name')  
        quantity = data.get('quantity')

        if not item_name or not quantity:
            # Validate presence of item name and quantity
            return JsonResponse({"status": "error", "message": "Both item name and quantity are required."}, status=400)

        try:
            # Create a new pantry item for the user
            new_item = PantryItem.objects.create(
                user=request.user,
                item_name=item_name,
                quantity=quantity
            )
            return JsonResponse({
                "status": "success",
                "item_id": new_item.id,
                "item": item_name,
                "quantity": quantity
            })
        except Exception as e:
            # Handle unexpected errors
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    # If the request method is not POST, return an error
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

@login_required
def add_utensil_item(request):
    """
    Add a new utensil item for the logged-in user.

    POST: Adds a new utensil item with the specified name and quantity.

    Args:
        request: The HTTP request object containing JSON data with 'utensil_name' and optional 'quantity'.

    Returns:
        JsonResponse: A success message with the created utensil's details or an error message.
    """
    if request.method == 'POST':
        data = json.loads(request.body)  
        utensil_name = data.get('utensil_name')  
        quantity = data.get('quantity', 1) 

        if not utensil_name or quantity <= 0:
            # Validate utensil name and ensure quantity is positive
            return JsonResponse({"status": "error", "message": "Invalid utensil name or quantity."})

        try:
            # Create a new utensil item for the user
            utensil = UtensilItem.objects.create(
                user=request.user,
                utensil_name=utensil_name,
                quantity=quantity
            )
            return JsonResponse({
                "status": "success",
                "utensil_id": utensil.id,
                "utensil": utensil.utensil_name,
                "quantity": utensil.quantity
            })
        except Exception as e:
            # Handle unexpected errors
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    # If the request method is not POST, return an error
    return JsonResponse({"status": "error", "message": "Invalid request method."})


def register(request):
    """
    Register a new user.

    POST: Processes user registration form and creates a new user.
    GET: Displays the registration form.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered registration page or redirects to the main welcome page after successful registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Create a form instance with the POST data
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log in the newly registered user
            return redirect('main_welcome')  # Redirect to the main welcome page
    else:
        form = UserCreationForm()  # Display an empty registration form
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    """
    Custom login view for user authentication.

    Attributes:
        template_name (str): Path to the login HTML template.
    """

    template_name = 'accounts/login.html'

    def get_success_url(self):
        """
        Get the URL to redirect to after successful login.

        Returns:
            str: URL to the main welcome page.
        """
        return reverse_lazy('main_welcome')


def custom_logout(request):
    """
    Log out the current user and redirect to the welcome page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirect to the welcome page.
    """
    logout(request) 
    return redirect('welcome')  # Redirect to the welcome page


@login_required
def fetch_calendar_events(request):
    """
    Fetch calendar events for the logged-in user.

    GET: Retrieves all calendar events for the user and returns them as JSON.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: List of user's calendar events.
    """
    events = CalendarEvent.objects.filter(user=request.user)  # Get user's calendar events
    event_list = [
        {
            "title": event.title,
            "start": event.date.isoformat(),
            "image": event.image,  # Optional field
        }
        for event in events
    ]
    return JsonResponse(event_list, safe=False)


@login_required
def add_to_calendar(request):
    """
    Add an event to the user's calendar.

    POST: Adds a new calendar event with details provided in the request.

    Args:
        request: The HTTP request object containing JSON data with event details.

    Returns:
        JsonResponse: A success message or an error message.
    """
    if request.method == "POST":
        data = json.loads(request.body)  
        title = data.get('title') 
        image = data.get('image') 
        recipe_id = data.get('recipe_id') 
        date = data.get('date') 
        meal_type = data.get('meal_type') 

        if not (title and date and meal_type):
            # Validate required fields
            return JsonResponse({"status": "error", "message": "Title, date, and meal type are required."}, status=400)

        try:
            # Generate recipe URL if a recipe ID is provided
            recipe_url = f"https://spoonacular.com/recipes/{title.replace(' ', '-')}-{recipe_id}" if recipe_id else None

            # Add the event to the calendar
            CalendarEvent.objects.create(
                user=request.user,
                title=title,
                image=image,
                recipe_id=recipe_id,
                recipe_url=recipe_url,
                date=date,
                meal_type=meal_type
            )
            return JsonResponse({"status": "success", "message": "Event added to calendar successfully."})
        except Exception as e:
            # Handle unexpected errors
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    # If the request method is not POST, return an error
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

@login_required
def generate_recipe(request):
    """
    Generate recipes based on the user's pantry items and preferences.

    POST: Fetches recipes from the Spoonacular API using the user's pantry items,
    cuisine preference, cooking time, and intolerances.

    Args:
        request: The HTTP request object containing JSON data with the user's preferences.

    Returns:
        JsonResponse: A list of recipes or an error message if the API request fails.
    """
    if request.method == "POST":
        data = json.loads(request.body)  
        recipe_count = data.get('recipe_count', 5)  
        cuisine = data.get('cuisine', None) 
        cooking_time = data.get('cooking_time', None) 
        intolerances = data.get('intolerances', []) 

        # Fetch user's pantry items
        pantry_items = list(PantryItem.objects.filter(user=request.user).values_list('item_name', flat=True))

        # Prepare API request parameters
        params = {
            "ingredients": ",".join(pantry_items),  # Comma-separated list of ingredients
            "number": recipe_count,
            "cuisine": cuisine if cuisine else None,  # Include cuisine if provided
            "maxReadyTime": cooking_time if cooking_time else None,  # Include max cooking time if provided
            "intolerances": ",".join(intolerances) if intolerances else None,  # Comma-separated intolerances
            "apiKey": settings.SPOONACULAR_API_KEY  # API key for Spoonacular
        }

        # Make API request to Spoonacular
        response = requests.get("https://api.spoonacular.com/recipes/findByIngredients", params=params)

        # Parse the API response
        if response.status_code == 200:
            recipes = response.json() 
            return JsonResponse({"recipes": recipes})
        else:
            # Handle API request failure
            return JsonResponse({"error": "Failed to fetch recipes."}, status=response.status_code)

    # Handle non-POST request
    return JsonResponse({"error": "Invalid request method."}, status=400)


@login_required
def schedule(request):
    """
    Render the schedule page.

    GET: Displays the user's schedule page.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered HTML page for the schedule.
    """
    return render(request, 'accounts/schedule.html')

@login_required
def fetch_calendar_events(request):
    """
    Fetch all calendar events for the logged-in user.

    GET: Retrieves all events and formats them for display in a calendar.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: List of events with details such as title, start date, and optional fields.
    """
    events = CalendarEvent.objects.filter(user=request.user)  # Fetch user's events
    event_list = [
        {
            "id": event.id,
            "title": event.title,
            "start": event.date.isoformat(),  # Convert date to ISO format
            "meal_type": event.meal_type,
            "image": event.image,
            "recipe_url": event.recipe_url,
        }
        for event in events
    ]

    return JsonResponse(event_list, safe=False)


@login_required
def delete_calendar_event(request):
    """
    Delete a calendar event for the logged-in user.

    POST: Deletes the specified calendar event based on its ID.

    Args:
        request: The HTTP request object containing JSON data with 'event_id'.

    Returns:
        JsonResponse: A success message or an error message if the event is not found.
    """
    if request.method == "POST":
        data = json.loads(request.body)  
        event_id = data.get('event_id')

        if not event_id:
            return JsonResponse({"status": "error", "message": "Event ID is required."}, status=400)

        try:
            event = CalendarEvent.objects.get(id=int(event_id), user=request.user)
            event.delete()  # Delete the event
            return JsonResponse({"status": "success", "message": "Event deleted successfully."})
        except ValueError:
            return JsonResponse({"status": "error", "message": "Invalid event ID."}, status=400)
        except CalendarEvent.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Event not found."}, status=404)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)


@login_required
def add_manual_calendar_event(request):
    """
    Add a manual calendar event for the logged-in user.

    POST: Adds a new event with a title, date, and meal type.

    Args:
        request: The HTTP request object containing JSON data with event details.

    Returns:
        JsonResponse: A success message or an error message if required fields are missing.
    """
    if request.method == "POST":
        data = json.loads(request.body) 
        title = data.get('title') 
        date = data.get('date') 
        meal_type = data.get('meal_type')

        if not (title and date and meal_type):
            return JsonResponse({"status": "error", "message": "Title, date, and meal type are required."}, status=400)

        # Create a new calendar event
        CalendarEvent.objects.create(
            user=request.user,
            title=title,
            date=date,
            meal_type=meal_type
        )

        return JsonResponse({"status": "success", "message": "Event added successfully."})

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)
