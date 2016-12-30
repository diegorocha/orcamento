from datetime import date
from orcamento import models
from model_mommy import mommy
from django.test import TestCase
from compras.models import Mercado
from django.core.urlresolvers import reverse
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
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data)
        for estatistica in data:
            self.assertIsNotNone(estatistica['categorias'])
            self.assertIsNotNone(estatistica['total'])
            self.assertIsNotNone(estatistica['orcamento'])

    def test_mercado(self):
        url = self.endpoint + 'mercado/'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data)
        self.assertIsNotNone(data['data'])
        self.assertIsNotNone(data['eixos'])

    def test_total(self):
        url = self.endpoint + 'total/'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data)
        self.assertIsNotNone(data['data'])
        self.assertIsNotNone(data['eixos'])

    def test_estatisticas_orcamento(self):
        orcamento = mommy.make(models.Orcamento)
        mommy.make(models.Conta, orcamento=orcamento, _quantity=5)
        url = self.get_detail_endpoint(orcamento.pk) + 'estatistica/'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
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
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertGreater(len(data), 0)
        for conta in data:
            self.assertIsNone(conta['categoria'])

    def test_ajustar(self):
        mommy.make(models.Conta, categoria=None, _quantity=5)
        url = self.endpoint + 'ajustar/'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertIsNone(data['categoria'])

    def test_ajustar_vazio(self):
        url = self.endpoint + 'ajustar/'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)


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
                '_selected_action': [unicode(conta.pk) for conta in contas]}
        response = self.client.post(url, data, follow=True)
        self.assertEquals(response.status_code, 200)


class OrcamentoTest(TestCase):
    def test_previsto_vazio(self):
        orcamento = mommy.make(models.Orcamento)
        self.assertEquals(orcamento.previsto, 0)

    def test_previsto(self):
        orcamento = mommy.make(models.Orcamento)
        contas = mommy.make(models.Conta, orcamento=orcamento, _fill_optional=['previsto'], _quantity=5)
        soma = sum([conta.previsto for conta in contas])
        self.assertEquals(orcamento.previsto, soma)

    def test_a_pagar_vazio(self):
        orcamento = mommy.make(models.Orcamento)
        self.assertEquals(orcamento.a_pagar, 0)

    def test_a_pagar(self):
        orcamento = mommy.make(models.Orcamento)
        contas = mommy.make(models.Conta, orcamento=orcamento, _fill_optional=['a_pagar'], _quantity=5)
        soma = sum([conta.a_pagar for conta in contas])
        self.assertEquals(orcamento.a_pagar, soma)

    def test_pago_vazio(self):
        orcamento = mommy.make(models.Orcamento)
        self.assertEquals(orcamento.pago, 0)

    def test_pago(self):
        orcamento = mommy.make(models.Orcamento)
        contas = mommy.make(models.Conta, orcamento=orcamento, _fill_optional=['pago'], _quantity=5)
        soma = sum([conta.pago for conta in contas])
        self.assertEquals(orcamento.pago, soma)

    def test_mercado_principal_vazio(self):
        orcamento = mommy.make(models.Orcamento)
        self.assertEquals(orcamento.mercado_principal, 0)

    def test_mercado_principal(self):
        orcamento = mommy.make(models.Orcamento)
        mercados = mommy.make(Mercado, orcamento=orcamento, tipo=0, _quantity=5)
        soma = sum([mercado.valor for mercado in mercados])
        self.assertEquals(orcamento.mercado_principal, soma)

    def test_mercado_outros_vazio(self):
        orcamento = mommy.make(models.Orcamento)
        mercados = mommy.make(Mercado, orcamento=orcamento, tipo=1, _quantity=5)
        soma = sum([mercado.valor for mercado in mercados])
        self.assertEquals(orcamento.mercado_outros, soma)


class OrcamentoAtualViewTest(LoginRequiredMixin, TestCase):
    def test_verify_redirect(self):
        hoje = date.today()
        url = reverse('orcamento:orcamento_atual')
        redirect_url = reverse('orcamento:orcamento', kwargs={'ano': hoje.year, 'mes': hoje.month})
        mommy.make(models.Orcamento, ano=hoje.year, mes=hoje.month)
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
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['object'], orcamento)
