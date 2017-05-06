from django.db.models import F, Q

from cartao.models import Fatura, CompraCartao


def fechar_fatura(fatura, orcamento, valor_final=None):
    if not fatura.aberta:
        raise Exception('Fatura já está fechada')
    if valor_final:
        fatura.valor_final = valor_final
    nova_fatura = Fatura(cartao=fatura.cartao, orcamento=orcamento)
    nova_fatura.save()
    for compra in fatura.compras.filter(Q(recorrente=True) | Q(parcelas__gt=1, parcela_atual__lt=F('parcelas'))):
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
        if compra.parcelas > 1:
            nova_compra.parcela_atual = compra.parcela_atual + 1
            nova_compra.parcelas = compra.parcelas
        nova_compra.save()
    fatura.aberta = False
    fatura.save()
    return nova_fatura