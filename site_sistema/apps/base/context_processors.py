from config.models import Logo, SEOHome


def context_social(request):
    return {'social': 'Exibir este contexto em qualquer lugar!'}


def get_logo(request):
    return {
        'logo': Logo.objects.all().first()
    }


def get_seo(request):
    return {
        'seo': SEOHome.objects.first()
    }