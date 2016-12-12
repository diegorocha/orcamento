# coding: utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from orcamento import models


class Command(BaseCommand):
    help = 'Copia as contas de um orçamento para outro'

    def add_arguments(self, parser):
        parser.add_argument('orcamento_origem', type=str)
        parser.add_argument('orcamento_destino', type=str)
        parser.add_argument(
            '--force', '-f',
            action='store_true',
            dest='force',
            default=False,
            help='Força a copia mesmo que o orçamento de destino já possua contas',
        )

    def handle(self, *args, **kwargs):
        origem = kwargs.get('orcamento_origem')
        destino = kwargs.get('orcamento_destino')
        ano_origem, mes_origem = origem.split('/')
        ano_destino, mes_destino = destino.split('/')
        orcamento_origem = models.Orcamento.objects.filter(ano=ano_origem, mes=mes_origem).first()
        if not orcamento_origem:
            raise CommandError('Orçamento "%s" não encontrado' % origem)
        contas = models.Conta.objects.filter(orcamento__ano=ano_origem, orcamento__mes=mes_origem, recorrente=True)
        orcamento_destino = models.Orcamento.objects.filter(ano=ano_destino, mes=mes_destino).first()
        contas_destino = models.Conta.objects.filter(orcamento__ano=ano_destino, orcamento__mes=mes_destino).count()
        if contas_destino == 0 or kwargs.get('force'):
            if not orcamento_destino:
                orcamento_destino = models.Orcamento()
                orcamento_destino.ano = int(ano_destino)
                orcamento_destino.mes = int(mes_destino)
                orcamento_destino.save()
            self.stdout.write('Copiando contas de %s para %s' % (orcamento_origem, orcamento_destino))
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
                    self.stdout.write('%s inserido.' % nova_conta)
        else:
            raise CommandError('Orçamento "%s" já possui contas. Use -f para forçar' % orcamento_destino)
