import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from base.utils import add_form_errors_to_messages

from .import models
from .forms import PostagemForumForm


# Lista de Postagens
def lista_postagem_forum(request):
    if request.path == '/forum/': # Pagina forum da home, mostrar tudo ativo.
        postagens = models.PostagemForum.objects.filter(ativo=True)
        template_view = 'lista-postagem-forum.html' # lista de post da rota /forum/
    else: # Essa parte mostra no Dashboard
        user = request.user
        lista_grupos = ['administrador', 'colaborador']
        print(user.groups.all()[0])
        template_view = 'dashboard/dash-lista-postagem-forum.html' # template novo que vamos criar 
        if any(grupo.name in lista_grupos for grupo in user.groups.all()) or user.is_superuser:
            # Usuário é administrador ou colaborador, pode ver todas as postagens
            postagens = models.PostagemForum.objects.all()
        else:
            # Usuário é do grupo usuário, pode ver apenas suas próprias postagens
            postagens = models.PostagemForum.objects.filter(usuario=user)
    # Como existe uma lista de objetos, para aparecer o formulário correspondente no modal precisamos ter um for
    form_dict = {}
    for el in postagens:
        form = PostagemForumForm(instance=el)
        form_dict[el] = form 
        
    # Criar uma lista de tuplas (postagem, form) a partir do form_dict
    form_list = [(postagem, form) for postagem, form in form_dict.items()]
    
    # Aplicar a paginação à lista de tuplas
    paginacao = Paginator(form_list, 3) # '3' é numero de registro por pagina
    
    # Obter o número da página a partir dos parâmetros da URL
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    
    # Criar um novo dicionário form_dict com base na página atual
    form_dict = {postagem: form for postagem, form in page_obj}
    
    context = {'page_obj': page_obj, 'form_dict': form_dict}
    return render(request, template_view, context)


# Formulario para Criar Postagens
def criar_postagem_forum(request):
    form = PostagemForumForm()
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES)
        if form.is_valid():
            postagem_imagens = request.FILES.getlist('postagem_imagens') # pega as imagens
            if len(postagem_imagens) > 5: # faz um count
                messages.error(request, 'Você pode adicionar no máximo 5 imagens.')
            else:
                forum = form.save(commit=False)
                forum.usuario = request.user
                form.save()
                
                for f in postagem_imagens:
                    models.PostagemForumImagem.objects.create(postagem=forum, imagem=f)

                # Redirecionar para uma página de sucesso ou fazer qualquer outra ação desejada
                messages.success(request, 'O seu Post foi cadastrado com sucesso!')
                return redirect('lista-postagem-forum')
        else:
            add_form_errors_to_messages
    return render(request, 'form-postagem-forum.html', {'form': form})


# Detalhe Postagem (ID)
def detalhe_postagem_forum(request, id):
    postagem = get_object_or_404(models.PostagemForum, id=id)
    form = PostagemForumForm(instance=postagem)
    context = {'form': form, 'postagem': postagem}
    return render(request, 'detalhe-postagem-forum.html', context)


# Editar Postagem (ID)
@login_required
def editar_postagem_forum(request, id):
    redirect_route = request.POST.get('redirect_route', '')
    postagem = get_object_or_404(models.PostagemForum, id=id)
    message = 'O seu Post: '+ postagem.titulo +', foi atualizado com sucesso!'
    # Verifica se o usuário autenticado é o autor da postagem
    lista_grupos = ['administrador', 'colaborador']
    if request.user != postagem.usuario and not (
        any(grupo.name in lista_grupos for grupo in request.user.groups.all()) or request.user.is_superuser):
        messages.warning(request, 'O seu usuário não tem permissões para acessar esta página.')
        return redirect('lista-postagem-forum')  # Redireciona para uma página de erro ou outra página adequada
    
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, instance=postagem)
        if form.is_valid():
            
            contar_imagens = postagem.postagem_imagens.count() # Quantidade de imagens sque já tenho no post
            postagem_imagens = request.FILES.getlist('postagem_imagens') # Quantidade de imagens que estou enviando para salvar

            if contar_imagens + len(postagem_imagens) > 5:
                messages.error(request, 'Você pode adicionar no máximo 5 imagens.')
                return redirect(redirect_route)
            else: 
                form.save()
                for f in postagem_imagens: # for para pegar as imagens e salvar.
                    models.PostagemForumImagem.objects.create(postagem=postagem, imagem=f)
                    
                messages.success(request, message)
                return redirect(redirect_route)
        else:
            add_form_errors_to_messages(request, form)
    
    return JsonResponse({'status': message}) # Coloca por enquanto.


# Deletar Postagem (ID)
@login_required 
def deletar_postagem_forum(request, id):
    redirect_route = request.POST.get('redirect_route', '')
    postagem = get_object_or_404(models.PostagemForum, id=id)
    message = 'O seu Post: '+ postagem.titulo +', foi deletado com sucesso!'    
    
    if request.method == 'POST':
        postagem.delete()
        messages.info(request, message)
        
        if re.search(r'/forum/detalhe-postagem-forum/([^/]+)/', redirect_route):
            return redirect('lista-postagem-forum')
        return redirect(redirect_route)

    return JsonResponse({'status': message})


def remover_imagem(request):
    imagem_id = request.GET.get('imagem_id') # Id da imagem
    verifica_imagem = models.PostagemForumImagem.objects.filter(id=imagem_id) # Filtra pra ver se imagem existe...
    if verifica_imagem:
        postagem_imagem = models.PostagemForumImagem.objects.get(id=imagem_id) # pega a imagem
        # Excluir a imagem do banco de dados e do sistema de arquivos (pasta postagem-forum/)
        postagem_imagem.imagem.delete()
        postagem_imagem.delete()
    return JsonResponse({'message': 'Imagem removida com sucesso!'})
