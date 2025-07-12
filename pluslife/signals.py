from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import LegendaImc

@receiver(post_migrate)
def criar_legendas_padrao(sender, **kwargs):
    if sender.name != 'pluslife':
        return

    legendas = [
        'Abaixo do peso',
        'Peso normal',
        'Sobrepeso',
        'Obesidade Grau 1',
        'Obesidade Grau 2',
        'Obesidade Grau 3',
    ]

    for titulo in legendas:
        LegendaImc.objects.get_or_create(titulo=titulo)
