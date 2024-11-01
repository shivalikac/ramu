from django.urls import path
from .views import welcome, CustomLoginView, register, login_welcome, profile, custom_logout

urlpatterns = [
    path('', welcome, name='welcome'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('main/', login_welcome, name='login_welcome'),  # URL for main welcome page
    path('logout/', custom_logout, name='logout'),
    path('profile/', profile, name='profile'),  # Profile page URL
]
