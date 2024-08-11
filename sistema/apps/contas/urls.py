from django.urls import path, include

from .views import *

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('timeout/',  timeout_view, name='timeout'),
    path('entrar/', login_view, name='login'),
    path('criar-conta/', register_view, name='register'),
    path('sair/', logout_view, name='logout'),
    path('atualizar-usuario/', atualizar_meu_usuario, name='atualizar_meu_usuario'),
    path('atualizar-usuario/<int:user_id>/', atualizar_usuario, name='atualizar_usuario'),
]
