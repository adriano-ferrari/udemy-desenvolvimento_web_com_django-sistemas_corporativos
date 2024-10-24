from django.contrib import admin
from .models import PostagemForum, PostagemForumImagem, PostagemForumComentario

class PostagemForumImagemInline(admin.TabularInline):
    model = PostagemForumImagem
    extra = 0

class PostagemForumAdmin(admin.ModelAdmin):
    inlines = [
        PostagemForumImagemInline,
    ]
    readonly_fields = ('slug',)


# Register your models here.
admin.site.register(PostagemForum, PostagemForumAdmin)
#admin.site.register(PostagemForumImagem)
admin.site.register(PostagemForumComentario)

