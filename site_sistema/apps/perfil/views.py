from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from contas.models import MyUser


login_required()
def perfil_view(request, username):
    fitro = MyUser.objects.select_related('perfil').prefetch_related('user_postagem_forum')
    perfil = get_object_or_404(fitro, username=username)
    context = {'obj': perfil}
    return render(request, 'perfil/perfil.html', context)
