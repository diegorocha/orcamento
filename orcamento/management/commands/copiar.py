# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError

from orcamento.utils import copiar_orcamento


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
        forcar = kwargs.get('force')
        _, erro = copiar_orcamento(origem, destino, forcar, self.stdout)
        if erro:
            raise CommandError(erro)
