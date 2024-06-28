# coding: utf-8
from compras.models import ListaCompras
from orcamento.models import Orcamento
from viagem.models import Viagem


def menu(request):
    return {
        'ultimos_orcamentos': Orcamento.objects.all()[:6],
        'ultimas_listas': ListaCompras.objects.all()[:3],
        'ultimas_viagens': Viagem.objects.all()[:4],
    }
