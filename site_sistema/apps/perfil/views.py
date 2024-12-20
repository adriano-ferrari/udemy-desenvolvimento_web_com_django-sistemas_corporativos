from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from base.utils import filtrar_modelo

from contas.models import MyUser
from contas.forms import UserChangeForm
from forum.forms import PostagemForumForm

from .models import Perfil
from .forms import PerfilForm


login_required()
def perfil_view(request, username):
    fitro = MyUser.objects.select_related('perfil').prefetch_related('user_postagem_forum')
    perfil = get_object_or_404(fitro, username=username)
    
    perfil_postagens = perfil.user_postagem_forum.all() # Todas as postagens relacionadas com perfil
    filtros = {} # Filtro dict

    valor_busca = request.GET.get("titulo") # Pego parametro
    if valor_busca:
        filtros["titulo"] = valor_busca # Adiciono no dicionario
        filtros["descricao"] = valor_busca
        
        # Utiliza o modelo das postagens do perfil
        perfil_postagens = filtrar_modelo(perfil_postagens, **filtros) # Faz o filtro

    form_dict = {}
    for el in perfil_postagens:
        form = PostagemForumForm(instance=el) 
        form_dict[el] = form
    
    # Criar uma lista de tuplas (postagem, form) a partir do form_dict
    form_list = [(postagem, form) for postagem, form in form_dict.items()]
    
    # Aplicar a paginação à lista de tuplas
    paginacao = Paginator(form_list, 3)
    
    # Obter o número da página a partir dos parâmetros da URL
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    
    # Criar um novo dicionário form_dict com base na página atual
    form_dict = {postagem: form for postagem, form in page_obj}
    context = {'obj': perfil, 'page_obj': page_obj, 'form_dict':form_dict}

    return render(request, 'perfil.html', context)


@login_required 
def editar_perfil(request, username):
    redirect_route = request.POST.get('redirect_route', '')

    modelo_myuser = MyUser.objects.get(username=username)
    modelo_perfil = Perfil.objects.get(usuario__username=username)
    
    message = 'O seu Perfil foi atualizado com sucesso!'
    
    if request.user.username != modelo_myuser.username and not (
        ['administrador', 'colaborador'] in request.user.groups.all() or request.user.is_superuser):
        return redirect('lista-postagem-forum')  # Adicionar uma rota "sem permissão"

    if request.method == 'POST':
        form_contas = UserChangeForm(request.POST, user=request.user, instance=modelo_myuser)
        form_perfil = PerfilForm(request.POST, request.FILES, instance=modelo_perfil)

        if form_perfil.is_valid() and form_contas.is_valid():
            form_contas.save()
            form_perfil.save()
            messages.warning(request, message)
            return redirect(redirect_route)
    else:
        form_contas = UserChangeForm(user=request.user, instance=modelo_myuser)
        form_perfil = PerfilForm(instance=modelo_perfil)

    context = {'form_perfil': form_perfil, 'form_contas': form_contas, 'obj': modelo_myuser}
    return render(request, 'editar-perfil-form.html', context)

