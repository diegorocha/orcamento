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
    for orcamento in models.Orcamento.objects.filter(mercados__isnull=False).distinct().order_by('-ano', '-mes')[:12].reverse():
        data['eixos'].append(str(orcamento))
        data['data'][0]['data'].append(orcamento.mercado_principal)
        data['data'][1]['data'].append(orcamento.mercado_outros)
    return data


def estatisticas_total():
    data = {'eixos': [],
            'data': [{'name': 'Previsto', 'data': []},
                     {'name': 'Final', 'data': []}]
           }
    for orcamento in models.Orcamento.objects.order_by('-ano', '-mes')[:12].reverse():
        data['eixos'].append(str(orcamento))
        data['data'][0]['data'].append(orcamento.previsto)
        data['data'][1]['data'].append(orcamento.atual)
    return data