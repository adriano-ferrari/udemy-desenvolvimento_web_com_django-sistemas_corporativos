from config.models import Logo


def context_social(request):
    return {'social': 'Exibir este contexto em qualquer lugar!'}


def get_logo(request):
    return {
        'logo': Logo.objects.all().first()
    }