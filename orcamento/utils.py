# coding: utf-8
from sys import stdout
from urllib.parse import urlunparse, urlparse, urlencode

from django.conf import settings

from orcamento import models


def estatisticas_orcamento(orcamento):
    if orcamento:
        categorias = list(models.Categoria.objects.all())
        total_orcamento = orcamento.atual
        estatistica_orcamento = {}
        estatistica_orcamento['orcamento'] = str(orcamento)
        estatistica_orcamento['total'] = float(total_orcamento)

        # Inicializa o valor total por categoria
        total_categorias = {}
        for categoria in categorias:
            total_categorias[categoria.descricao] = 0
        total_categorias['Outros'] = 0

        # Separa o valor de cada conta
        for conta in orcamento.contas.all():
            if conta.categoria:
                total_categorias[conta.categoria.descricao] += conta.atual
            else:
                total_categorias['Outros'] += conta.atual
        estatisticas_categorias = []

        # Calcula os totais
        for categoria_ in total_categorias.keys():
            total_categoria = total_categorias[categoria_]
            estatistica_categoria = {'categoria': categoria_}
            estatistica_categoria['total'] = float(total_categoria)
            estatistica_categoria['percentual'] = float(total_categoria / total_orcamento * 100)
            estatisticas_categorias.append(estatistica_categoria)
        estatistica_orcamento['categorias'] = estatisticas_categorias
        return estatistica_orcamento


def gerar_estatisticas():
    estatisticas = []
    for orcamento in models.Orcamento.objects.order_by('-ano', '-mes')[:12]:
        estatisticas.append(estatisticas_orcamento(orcamento))
    return estatisticas


def estatisticas_mercado():
    data = {'eixos': [],
            'data': [{'name': 'Principal', 'data': []},
                     {'name': 'Outros', 'data': []}]
           }
    for orcamento in models.Orcamento.objects.filter(mercados__isnull=False).distinct()[:12:-1]:
        data['eixos'].append(str(orcamento))
        data['data'][0]['data'].append(orcamento.mercado_principal)
        data['data'][1]['data'].append(orcamento.mercado_outros)
    return data


def estatisticas_total():
    data = {'eixos': [],
            'data': [{'name': 'Previsto', 'data': []},
                     {'name': 'Final', 'data': []}]
           }
    for orcamento in models.Orcamento.objects.all()[:12:-1]:
        data['eixos'].append(str(orcamento))
        data['data'][0]['data'].append(orcamento.previsto)
        data['data'][1]['data'].append(orcamento.atual)
    return data


def copiar_orcamento(origem, destino, forcar=False, out=None):
    ano_origem, mes_origem = origem.split('/')
    ano_destino, mes_destino = destino.split('/')
    if not out:
        out = stdout
    orcamento_origem = models.Orcamento.objects.filter(ano=ano_origem, mes=mes_origem).first()
    if not orcamento_origem:
        return False, 'Orçamento "%s" não encontrado' % origem
    contas = models.Conta.objects.filter(orcamento__ano=ano_origem, orcamento__mes=mes_origem, recorrente=True)
    orcamento_destino = models.Orcamento.objects.filter(ano=ano_destino, mes=mes_destino).first()
    contas_destino = models.Conta.objects.filter(orcamento__ano=ano_destino, orcamento__mes=mes_destino).count()
    if contas_destino == 0 or forcar:
        if not orcamento_destino:
            orcamento_destino = models.Orcamento()
            orcamento_destino.ano = int(ano_destino)
            orcamento_destino.mes = int(mes_destino)
            orcamento_destino.save()
        out.write('Copiando contas de %s para %s' % (orcamento_origem, orcamento_destino))
        for conta in contas:
            if conta.parcelas == 1 or conta.parcela_atual < conta.parcelas:
                nova_conta = models.Conta()
                nova_conta.orcamento = orcamento_destino
                nova_conta.nome = conta.nome
                nova_conta.descricao = conta.descricao
                nova_conta.previsto = conta.previsto
                nova_conta.categoria = conta.categoria
                if conta.parcelas > 1:
                    nova_conta.parcela_atual = conta.parcela_atual + 1
                nova_conta.parcelas = conta.parcelas
                nova_conta.recorrente = conta.recorrente
                nova_conta.save()
                out.write('%s inserido.' % nova_conta)
        return True, None
    else:
        return False, 'Orçamento "%s" já possui contas' % orcamento_destino


def get_contas_url(orcamento, user):
    parts = urlparse(settings.CONTAS_URL)
    data = {
        'id': orcamento.id,
        't': user.auth_token.key,
    }
    return urlunparse(parts._replace(query=urlencode(data)))
