from django.urls import path
from .views import *


urlpatterns = [
    path('<slug:username>/', perfil_view, name='perfil'),
    path('editar-perfil/<slug:username>/', editar_perfil, name='editar-perfil'),
]
