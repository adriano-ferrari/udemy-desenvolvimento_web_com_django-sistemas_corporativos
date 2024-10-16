from django.shortcuts import redirect, render
from django.contrib import messages

from base.utils import add_form_errors_to_messages

from .import models
from .forms import PostagemForumForm


# Create your views here.
def lista_postagem_forum(request):
    postagens = models.PostagemForum.objects.filter(ativo=True)
    context = {'postagens': postagens}
    return render(request, 'forum/lista-postagem-forum.html', context)
  

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