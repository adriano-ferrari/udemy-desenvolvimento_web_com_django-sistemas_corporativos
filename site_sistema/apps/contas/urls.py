from django.urls import path, include
from .import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),  # Django auth
    path('timeout/',  views.timeout_view, name='timeout'),
    path('entrar/', views.login_view, name='login'),
    path('sair/', views.logout_view, name='logout'),
    path('criar-conta/', views.register_view, name='register'),
    path('atualizar-usuario/', views.atualizar_meu_usuario, name='atualizar_meu_usuario'),
    path('atualizar-usuario/<int:user_id>/', views.atualizar_usuario, name='atualizar_usuario'),
]
