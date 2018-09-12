# coding: utf-8
from re import match

from django.db.models import F, Q, Sum

from cartao.models import Fatura, CompraCartao, CartaoAliasSMS
from orcamento.models import Categoria


def get_queryset_proxima_fatura(queryset):
    if queryset:
        return queryset.filter(Q(recorrente=True) | Q(parcelas__gt=1, parcela_atual__lt=F('parcelas')))


def fechar_fatura(fatura, orcamento, valor_final=None):
    if not fatura.aberta:
        raise Exception('Fatura já está fechada')
    if valor_final:
        fatura.valor_final = valor_final
    nova_fatura = Fatura(cartao=fatura.cartao, orcamento=orcamento)
    nova_fatura.save()
    compras, _ = fatura.get_compras_proxima_fatura()
    for compra in compras:
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


def parse_sms(sms):
    regex_list = [
        r'(?P<tipo>Compra|Pre-autorizacao) aprovada no seu (?P<cartao>[\w\s\.]*) - (?P<descricao_fatura>.*) valor (?P<moeda>.*) (?P<valor>.*) em.*'
    ]
    data = {}
    for regex in regex_list:
        result = match(regex, sms.texto)
        if result:
            groups = result.groupdict()
            cartao_alias = groups.get('cartao')
            if cartao_alias:
                alias = CartaoAliasSMS.objects.filter(texto__iexact=cartao_alias).first()
                if alias:
                    fatura = alias.cartao.faturas.filter(aberta=True).first()
                    data['fatura_id'] = fatura.id if fatura else None
                    # Ajuste dos dados
                    data['sms_id'] = sms.id
                    data['sms'] = sms.texto
                    data['moeda'] = groups.get('moeda', '')
                    data['descricao_fatura'] = groups.get('descricao_fatura', '').title()
                    data['valor'] = float(groups.get('valor', '0').replace(',', '.'))
                return data
    return data
