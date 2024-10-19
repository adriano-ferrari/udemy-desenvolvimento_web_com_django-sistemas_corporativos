from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from base.utils import add_form_errors_to_messages

from .import models
from .forms import PostagemForumForm


# Lista de Postagens
def lista_postagem_forum(request):
    postagens = models.PostagemForum.objects.filter(ativo=True)
    context = {'postagens': postagens}
    return render(request, 'forum/lista-postagem-forum.html', context)
  

# Formulario para Criar Postagens
def criar_postagem_forum(request):
    form = PostagemForumForm()
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.usuario = request.user
            form.save()
            # Redirecionar para uma página de sucesso ou fazer qualquer outra ação desejada
            messages.success(request, 'O seu Post foi cadastrado com sucesso!')
            return redirect('lista-postagem-forum')
        else:
            add_form_errors_to_messages
    return render(request, 'forum/form-postagem-forum.html', {'form': form})


# Detalhe Postagem (ID)
def detalhe_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    return render(request, 'forum/detalhe-postagem-forum.html', {'postagem': postagem})


# Editar Postagem (ID)
@login_required
def editar_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    
    # Verifica se o usuário autenticado é o autor da postagem
    if request.user != postagem.usuario and not (
            ['administrador', 'colaborador'] in request.user.groups.all() 
						or request.user.is_superuser):
            
            messages.warning(request, 'O seu usuario nao tem permissao para acessar esta pagina!')
            # Redireciona para uma página de erro ou outra página adequada
            return redirect('lista-postagem-forum')  
    
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, instance=postagem)
        if form.is_valid():
            form.save()
            messages.success(request, 'O seu Post '+ postagem.titulo +' \
                foi atualizado com sucesso!')
            return redirect('editar-postagem-forum', id=postagem.id)
        else:
            add_form_errors_to_messages(request, form)
    else:
        form = PostagemForumForm(instance=postagem)
    return render(request, 'forum/form-postagem-forum.html', {'form': form})


# Deletar Postagem (ID)
@login_required 
def deletar_postagem_forum(request, id): 
    postagem = get_object_or_404(models.PostagemForum, id=id)
    print(postagem)
    if request.method == 'POST':
        postagem.delete()
        messages.error(request, 'O seu Post: '+ postagem.titulo +'. Foi deletado com sucesso!')
        return redirect('lista-postagem-forum')
    return render(request, 'forum/detalhe-postagem-forum.html', 
                  {'postagem': postagem})


def lista_postagem_forum(request):
    if request.path == '/forum/': # Pagina forum da home, mostrar tudo ativo.
        postagens = models.PostagemForum.objects.filter(ativo=True)
        template_view = 'lista-postagem-forum.html' # lista de post da rota /forum/
    else: # Essa parte mostra no Dashboard
        user = request.user 
        template_view = 'forum/dashboard/dash-lista-postagem-forum.html' # template novo que vamos criar 
        if ['administrador', 'colaborador'] in user.groups.all() or user.is_superuser:
            # Usuário é administrador ou colaborador, pode ver todas as postagens
            postagens = models.PostagemForum.objects.filter(ativo=True)
        else:
            # Usuário é do grupo usuário, pode ver apenas suas próprias postagens
            postagens = models.PostagemForum.objects.filter(usuario=user)
    context = {'postagens': postagens}
    return render(request, template_view, context)