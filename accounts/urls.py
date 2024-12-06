from django.urls import path
from .views import (
    welcome, CustomLoginView, register, main_welcome, profile, custom_logout, 
    add_pantry_item, add_utensil_item, delete_pantry_item, delete_utensil_item,  
    generate_recipe, schedule, fetch_calendar_events, add_to_calendar,  
    delete_calendar_event, add_manual_calendar_event, recipe_notes, 
    add_grocery_shopping_event, grocery_notes 
)

# Define URL patterns
urlpatterns = [
    path('', welcome, name='welcome'),  # URL for the welcome page (default home)
    path('login/', CustomLoginView.as_view(), name='login'),  # URL for the login page
    path('register/', register, name='register'),  # URL for the user registration page
    path('main/', main_welcome, name='main_welcome'),  # URL for the main welcome page
    path('logout/', custom_logout, name='logout'),  # URL to log out a user
    path('profile/', profile, name='profile'),  # URL for the user profile page

    # Pantry item management URLs
    path('add_pantry_item/', add_pantry_item, name='add_pantry_item'),
    path('delete_pantry_item/', delete_pantry_item, name='delete_pantry_item'),

    # Utensil item management URLs
    path('add_utensil_item/', add_utensil_item, name='add_utensil_item'), 
    path('delete_utensil_item/', delete_utensil_item, name='delete_utensil_item'), 

    # Recipe management URLs
    path('generate_recipe/', generate_recipe, name='generate_recipe'), 

    # Calendar and scheduling URLs
    path('schedule/', schedule, name='schedule'),  # Display the schedule page
    path('fetch_calendar_events/', fetch_calendar_events, name='fetch_calendar_events'),  
    path('add_to_calendar/', add_to_calendar, name='add_to_calendar'),  
    path('delete_calendar_event/', delete_calendar_event, name='delete_calendar_event'), 
    path('add_manual_calendar_event/', add_manual_calendar_event, name='add_manual_calendar_event'), 

    # Event-specific note-taking URLs
    path('recipe_notes/<int:event_id>/', recipe_notes, name='recipe_notes'),  # Add/view notes for a recipe event
    path('add_grocery_shopping_event/', add_grocery_shopping_event, name='add_grocery_shopping_event'),  # Add grocery shopping event
    path('grocery_notes/<int:event_id>/', grocery_notes, name='grocery_notes'),  # Add/view notes for a grocery event
]
