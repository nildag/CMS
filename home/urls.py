from django.urls import path
from .views import home, profile, administrar

urlpatterns = [
    path("", home, name='home'),
    path('accounts/profile/', profile, name='profile'),
    path('administrar/', administrar, name='administrar'),
]