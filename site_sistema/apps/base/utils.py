from django.contrib import messages


def add_form_errors_to_messages(request, form):
    for field, error_list in form.errors.items():
        for error in error_list:
            messages.error(request, f"Erro no campo '{form[field].label}': {error}")


def filtrar_modelo(modelo, **filtros):
    queryset = modelo.objects.all()
    for campo, valor in filtros.items():
        lookup = f'{campo}__icontains'
        queryset = queryset.filter(**{lookup: valor})
    return queryset
