from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from contas.models import MyUser


login_required()
def perfil_view(request, username):
    perfil = get_object_or_404(MyUser.objects.select_related('perfil'), username=username)
    context = {'obj': perfil}
    return render(request, 'perfil/perfil.html', context)