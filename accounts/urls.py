from django.urls import path
from .views import welcome, CustomLoginView, register, main_welcome, profile, custom_logout, add_pantry_item, add_utensil_item
from .views import delete_pantry_item, delete_utensil_item, generate_recipe, schedule, link_calendar, oauth_callback, fetch_calendar_events
from .views import add_to_calendar, recipe_notes

from .views import (
    schedule,
    fetch_calendar_events,
    add_to_calendar,
    delete_calendar_event,  # Make sure this is imported
    add_manual_calendar_event,
)

urlpatterns = [
    path('', welcome, name='welcome'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('main/', main_welcome, name='main_welcome'),  # URL for main welcome page
    path('logout/', custom_logout, name='logout'),
    path('profile/', profile, name='profile'),  # Profile page URL
    path('add_pantry_item/', add_pantry_item, name='add_pantry_item'),
    path('add_utensil_item/', add_utensil_item, name='add_utensil_item'),
    path('delete_pantry_item/', delete_pantry_item, name='delete_pantry_item'),
    path('delete_utensil_item/', delete_utensil_item, name='delete_utensil_item'),
    path('generate_recipe/', generate_recipe, name='generate_recipe'),
    path('schedule/', schedule, name='schedule'),
    path('link_calendar/<str:calendar_type>/', link_calendar, name='link_calendar'),
    path('oauth_callback/<str:calendar_type>/', oauth_callback, name='oauth_callback'),
    path('fetch_calendar_events/', fetch_calendar_events, name='fetch_calendar_events'),
    path('add_to_calendar/', add_to_calendar, name='add_to_calendar'),
    path('delete_calendar_event/', delete_calendar_event, name='delete_calendar_event'),
    path('add_manual_calendar_event/', add_manual_calendar_event, name='add_manual_calendar_event'),
    path('recipe_notes/<int:event_id>/', recipe_notes, name='recipe_notes'),
]
