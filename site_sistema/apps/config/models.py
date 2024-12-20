from django.db import models
from django.core.exceptions import ValidationError


class Logo(models.Model):
    title = models.CharField('Título/Alt', max_length=100)
    image = models.ImageField('Logo', upload_to='images')

    class Meta:
        verbose_name = 'Logo'
        verbose_name_plural = 'Logo'

    def __str__(self):
        return self.title

    def clean(self):
        model = self.__class__
        if model.objects.count() >= 2 and not self.pk:
            raise ValidationError('Já existe uma 2ª logomarca cadastrada.')
        

class SEOHome(models.Model):
    meta_description = models.CharField('Meta descrição', max_length=255)
    meta_keywords = models.CharField('Palavras chaves', max_length=255, help_text='Separadas por virgula')

    class Meta:
        verbose_name = 'SEO Home'
        verbose_name_plural = 'SEO Home'

    def __str__(self) -> str:
        return 'Meta tags da Página Home'

    def clean(self):
        model = self.__class__
        if model.objects.exists() and self.pk != model.objects.first().pk:
            raise ValidationError('Já existe meta tags cadastradas para a Home.')