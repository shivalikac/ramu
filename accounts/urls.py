from django.urls import path
from .views import welcome, CustomLoginView, register, main_welcome, profile, custom_logout, add_pantry_item, add_utensil_item
from .views import delete_pantry_item, delete_utensil_item, generate_recipe

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
]
