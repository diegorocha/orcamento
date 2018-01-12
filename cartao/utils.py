# coding: utf-8
from django.db.models import F, Q, Sum

from cartao.models import Fatura, CompraCartao
from orcamento.models import Categoria


def _incrementa_parcela(compra, n=1):
    if compra:
        if compra.parcelas > 1:
            compra.parcela_atual += n
            if compra.parcela_atual > compra.parcelas:
                return
    return compra


def get_queryset_proxima_fatura(queryset):
    if queryset:
        return queryset.filter(Q(recorrente=True) | Q(parcelas__gt=1, parcela_atual__lt=F('parcelas')))


def get_compras_proxima_fatura(queryset, n=1, incluir_totais=False):
    if queryset:
        compras = []
        totais = dict(valor_real=0, valor_dolar=0, valor_fatura=0)
        for compra in get_queryset_proxima_fatura(queryset):
            nova_compra = _incrementa_parcela(compra, n)
            if nova_compra:
                compras.append(nova_compra)
                try:
                    totais['valor_real'] += nova_compra.valor_real
                    totais['valor_dolar'] += nova_compra.valor_dolar
                    totais['valor_fatura'] += nova_compra.valor_fatura
                except:
                    pass
        if incluir_totais:
            return compras, totais
        return compras


def fechar_fatura(fatura, orcamento, valor_final=None):
    if not fatura.aberta:
        raise Exception('Fatura já está fechada')
    if valor_final:
        fatura.valor_final = valor_final
    nova_fatura = Fatura(cartao=fatura.cartao, orcamento=orcamento)
    nova_fatura.save()
    for compra in get_compras_proxima_fatura(fatura.compras):
        nova_compra = CompraCartao()
        nova_compra.fatura = nova_fatura
        nova_compra.descricao = compra.descricao
        nova_compra.valor_real = compra.valor_real
        nova_compra.valor_dolar = compra.valor_dolar
        nova_compra.valor_inicial = compra.valor_inicial
        nova_compra.valor_fatura = compra.valor_fatura
        nova_compra.valor_final = compra.valor_final
        nova_compra.categoria = compra.categoria
        nova_compra.recorrente = compra.recorrente
        nova_compra.parcela_atual = compra.parcela_atual
        nova_compra.parcelas = compra.parcelas
        nova_compra.save()
    fatura.aberta = False
    fatura.save()
    return nova_fatura


def estatistica_fatura(fatura):
    estatistica = dict([(c['descricao'], 0) for c in Categoria.objects.values('descricao')])
    if fatura and fatura.compras:
        for categoria in fatura.compras.values('categoria__descricao').annotate(valor=Sum('valor_inicial')):
            descricao = categoria['categoria__descricao']
            valor = categoria.get('valor', 0)
            estatistica[descricao] = valor
    return estatistica
