from orcamento import models
from model_mommy import mommy
from django.test import TestCase
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
