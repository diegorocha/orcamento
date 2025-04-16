# coding=utf-8
from __future__ import unicode_literals

from datetime import date, timedelta
from io import StringIO
from random import randrange

from django.core.management import CommandError
from django.core.management import call_command

from orcamento import models
from model_mommy import mommy
from django.test import TestCase
from compras.models import Mercado
from django.urls import reverse
from core.tests import LoginRequiredMixin, ModelViewSetTestCase


class OrcamentoViewSetTest(LoginRequiredMixin, ModelViewSetTestCase):
    url_base_name = 'api:orcamento'
    model_name = models.Orcamento

    def create_data(self):
        return {'ano': 1991, 'mes': 6}

    def update_data(self):
        return {'mes': 7}

    def test_estatisticas(self):
        url = self.endpoint + 'estatisticas/'
        orcamento = mommy.make(models.Orcamento)
        categoria = mommy.make(models.Categoria)
        conta_com_categoria = mommy.make(models.Conta, orcamento=orcamento, categoria=categoria)
        conta_sem_categoria = mommy.make(models.Conta, orcamento=orcamento, categoria=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data)
        for estatistica in data:
            self.assertIsNotNone(estatistica['orcamento'])
            self.assertEqual(estatistica['orcamento'], str(orcamento))
            self.assertIsNotNone(estatistica['total'])
            self.assertEqual(estatistica['total'], float(orcamento.previsto))
            self.assertIsNotNone(estatistica['categorias'])
            self.assertEqual(len(estatistica['categorias']), models.Categoria.objects.count() + 1)
            for categoria in estatistica['categorias']:
                self.assertIsNotNone(categoria['categoria'])
                self.assertIsNotNone(categoria['percentual'])
                self.assertIsNotNone(categoria['total'])

    def test_mercado(self):
        url = self.endpoint + 'mercado/'
        for orcamento in mommy.make(models.Orcamento, _quantity=18):
            mommy.make(Mercado, orcamento=orcamento, tipo=0)
            mommy.make(Mercado, orcamento=orcamento, tipo=1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data)
        self.assertIsNotNone(data['eixos'])
        self.assertEqual(len(data['eixos']), 12)
        self.assertIsNotNone(data['data'])
        for data in data['data']:
            self.assertIsNotNone(data['name'])
            self.assertIsNotNone(data['data'])

    def test_total(self):
        url = self.endpoint + 'total/'
        for orcamento in mommy.make(models.Orcamento, _quantity=18):
            mommy.make(models.Conta, orcamento=orcamento)
            mommy.make(models.Conta, orcamento=orcamento)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data)
        self.assertIsNotNone(data['eixos'])
        self.assertEqual(len(data['eixos']), 12)
        self.assertIsNotNone(data['data'])
        for data in data['data']:
            self.assertIsNotNone(data['name'])
            self.assertIsNotNone(data['data'])


    def test_estatisticas_orcamento(self):
        orcamento = mommy.make(models.Orcamento)
        mommy.make(models.Conta, orcamento=orcamento, _quantity=5)
        url = self.get_detail_endpoint(orcamento.pk) + 'estatistica/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data)
        self.assertIsNotNone(data['categorias'])
        self.assertIsNotNone(data['total'])
        self.assertIsNotNone(data['orcamento'])


class ContaViewSetTest(LoginRequiredMixin, ModelViewSetTestCase):
    url_base_name = 'api:conta'
    model_name = models.Conta

    def create_data(self):
        orcamento = mommy.make(models.Orcamento)
        return {'orcamento': orcamento.pk, 'nome': 'Test', 'descricao': 'Test Description', 'previsto': 100}

    def update_data(self):
        return {'descricao': 'Another Description'}

    def test_sem_categoria(self):
        mommy.make(models.Conta, categoria=None, _quantity=5)
        url = self.endpoint + 'sem_categoria/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(len(data), 0)
        for conta in data:
            self.assertIsNone(conta['categoria'])

    def test_ajustar(self):
        mommy.make(models.Conta, categoria=None, _quantity=5)
        url = self.endpoint + 'ajustar/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNone(data['categoria'])

    def test_ajustar_vazio(self):
        url = self.endpoint + 'ajustar/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ContaAdminTest(LoginRequiredMixin, TestCase):
    def test_acertar_situacao(self):
        orcamento = mommy.make(models.Orcamento)
        contas = []
        for i in range(10):
            valor = i * 100
            conta = models.Conta.objects.create(orcamento=orcamento, nome='Test %d' % i, previsto=valor, atual=valor, pago=valor)
            contas.append(conta)
        models.Conta.objects.filter(nome__startswith='Test').update(situacao=0)
        url = reverse('admin:orcamento_conta_changelist')
        data = {'action': 'acertar_situacao',
                '_selected_action': [str(conta.pk) for conta in contas]}
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)


class OrcamentoTest(TestCase):
    def test_previsto_vazio(self):
        orcamento = mommy.make(models.Orcamento)
        self.assertEqual(orcamento.previsto, 0)

    def test_previsto(self):
        orcamento = mommy.make(models.Orcamento)
        contas = mommy.make(models.Conta, orcamento=orcamento, _fill_optional=['previsto'], _quantity=5)
        soma = sum([conta.previsto for conta in contas])
        self.assertEqual(orcamento.previsto, soma)

    def test_a_pagar_vazio(self):
        orcamento = mommy.make(models.Orcamento)
        self.assertEqual(orcamento.a_pagar, 0)

    def test_a_pagar(self):
        orcamento = mommy.make(models.Orcamento)
        contas = mommy.make(models.Conta, orcamento=orcamento, _fill_optional=['a_pagar'], _quantity=5)
        soma = sum([conta.a_pagar for conta in contas])
        self.assertEqual(orcamento.a_pagar, soma)

    def test_pago_vazio(self):
        orcamento = mommy.make(models.Orcamento)
        self.assertEqual(orcamento.pago, 0)

    def test_pago(self):
        orcamento = mommy.make(models.Orcamento)
        contas = mommy.make(models.Conta, orcamento=orcamento, _fill_optional=['pago'], _quantity=5)
        soma = sum([conta.pago for conta in contas])
        self.assertEqual(orcamento.pago, soma)

    def test_mercado_principal_vazio(self):
        orcamento = mommy.make(models.Orcamento)
        self.assertEqual(orcamento.mercado_principal, 0)

    def test_mercado_principal(self):
        orcamento = mommy.make(models.Orcamento)
        mercados = mommy.make(Mercado, orcamento=orcamento, tipo=0, _quantity=5)
        soma = sum([mercado.valor for mercado in mercados])
        self.assertEqual(orcamento.mercado_principal, soma)

    def test_mercado_outros_vazio(self):
        orcamento = mommy.make(models.Orcamento)
        mercados = mommy.make(Mercado, orcamento=orcamento, tipo=1, _quantity=5)
        soma = sum([mercado.valor for mercado in mercados])
        self.assertEqual(orcamento.mercado_outros, soma)


class OrcamentoAtualViewTest(LoginRequiredMixin, TestCase):
    def test_verify_redirect_without_orcamento_default(self):
        hoje = date.today()
        url = reverse('orcamento:home')
        redirect_url = reverse('orcamento:orcamento', kwargs={'ano': hoje.year, 'mes': hoje.month})
        mommy.make(models.Orcamento, ano=hoje.year, mes=hoje.month)
        response = self.client.get(url)
        self.assertRedirects(response, redirect_url)

    def test_verify_redirect_with_orcamento_default(self):
        data = date.today() + timedelta(days=30)
        url = reverse('orcamento:home')
        redirect_url = reverse('orcamento:orcamento', kwargs={'ano': data.year, 'mes': data.month})
        orcamento = mommy.make(models.Orcamento, ano=data.year, mes=data.month)
        mommy.make(models.OrcamentoDefault, orcamento=orcamento)
        response = self.client.get(url)
        self.assertRedirects(response, redirect_url)


class ListaViewTest(LoginRequiredMixin, TestCase):
    def test_get(self):
        orcamento = mommy.make(models.Orcamento)
        orcamento.ano = abs(orcamento.ano)
        orcamento.mes = abs(orcamento.mes)
        orcamento.save()
        url = reverse('orcamento:orcamento', kwargs={'ano': orcamento.ano, 'mes': orcamento.mes})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], orcamento)


class EstatisticaViewTest(LoginRequiredMixin, TestCase):
    def test_get(self):
        url = reverse('orcamento:estatistica')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class CopiarTest(TestCase):
    def test_orcamento_nao_existe(self):
        args = ['1234/12', '1234/13']
        opts = {}
        with self.assertRaises(CommandError):
            call_command('copiar', *args, **opts)

    def test_orcamento_destino_com_contas(self):
        origem = mommy.make(models.Orcamento)
        destino = mommy.make(models.Orcamento)
        mommy.make(models.Conta, orcamento=destino)
        args = [str(origem), str(destino)]
        opts = {}
        with self.assertRaises(CommandError):
            call_command('copiar', *args, **opts)

    def test_copiar_apenas_recorrente(self):
        origem = mommy.make(models.Orcamento)
        qtd_recorrente = randrange(10, 20)
        mommy.make(models.Conta, orcamento=origem, recorrente=True, _quantity=qtd_recorrente)
        mommy.make(models.Conta, orcamento=origem, recorrente=False, _quantity=randrange(10, 20))
        novo = {'ano': origem.ano, 'mes': origem.mes + 1}
        args = [str(origem), '%(ano)d/%(mes)d' % novo]
        with StringIO() as out:
            opts = {
                'stdout': out,
            }
            call_command('copiar', *args, **opts)
        destino = models.Orcamento.objects.get(**novo)
        self.assertIsNotNone(destino)
        self.assertEqual(destino.contas.count(), qtd_recorrente)

    def test_copiar_nao_copia_ultima_parcela(self):
        origem = mommy.make(models.Orcamento)
        qtd_recorrente = randrange(10, 20)
        contas = mommy.make(models.Conta, orcamento=origem, recorrente=True, _quantity=qtd_recorrente)
        mommy.make(models.Conta, orcamento=origem, recorrente=False, _quantity=randrange(10, 20))
        mommy.make(models.Conta, orcamento=origem, recorrente=True, parcelas=3, parcela_atual=3)  # Não deve ser copiado
        contas[0].parcelas = 3
        contas[0].parcela = 1
        contas[0].save()
        novo = {'ano': origem.ano, 'mes': origem.mes + 1}
        args = [str(origem), '%(ano)d/%(mes)d' % novo]
        with StringIO() as out:
            opts = {
                'stdout': out,
            }
            call_command('copiar', *args, **opts)
        destino = models.Orcamento.objects.get(**novo)
        self.assertIsNotNone(destino)
        self.assertEqual(destino.contas.count(), qtd_recorrente)


class ListaOrcamentoViewTest(LoginRequiredMixin, TestCase):
    def test_get(self):
        qtd_orcamento = randrange(13, 20)
        mommy.make(models.Orcamento, _quantity=qtd_orcamento)
        url = reverse('orcamento:orcamentos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['itens']), qtd_orcamento)

    def test_get_empty(self):
        empty_message = u'Nenhum orçamento cadastrado'.encode('utf-8')
        url = reverse('orcamento:orcamentos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['itens']), 0)
        self.assertIn(empty_message, response.content)


class OrcamentoDefaultModelTest(TestCase):
    def test_must_have_just_one(self):
        mommy.make(models.OrcamentoDefault)
        second = mommy.make(models.OrcamentoDefault)
        self.assertEqual(models.OrcamentoDefault.objects.count(), 1)
        self.assertEqual(models.OrcamentoDefault.objects.first().pk, second.pk)
