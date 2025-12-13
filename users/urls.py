from django.urls import path
from .views import login_view, RegisterView, logout_view, ProfileView, create_admin_once

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('create-admin/', create_admin_once),  # 👈 TEMP
]
