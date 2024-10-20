# Generated by Django 4.2.2 on 2024-10-20 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostagemForumImagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.FileField(upload_to='postagem-forum/', verbose_name='Imagem Anexo')),
                ('postagem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postagem_imagens', to='forum.postagemforum')),
            ],
        ),
    ]
