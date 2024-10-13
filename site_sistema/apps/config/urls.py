from django.urls import path 
from .import views


urlpatterns = [
    path('', views.painel_view, name='painel'),
    path('configuracao/', views.configuracao_view, name='configuracao'), 
]