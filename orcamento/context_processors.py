# coding: utf-8
from compras.models import ListaCompras
from orcamento.models import Orcamento


def menu(request):
    return {
        'ultimos_orcamentos': Orcamento.objects.all()[:4],
        'ultimas_listas': ListaCompras.objects.all()[:3]
    }