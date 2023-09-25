from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    path('verUsuarios/', views.verUsuarios, name='verUsuarios'),
]
