from datetime import date
from random import randrange
from model_mommy import mommy
from django.test import TestCase
from orcamento.models import Orcamento
from django.urls import reverse
from core.tests import LoginRequiredMixin, ModelViewSetTestCase
from compras.models import Mercado, SecaoLista, ItensLista, ListaCompras, ItemCompra


class MercadoViewSetTest(LoginRequiredMixin, ModelViewSetTestCase):
    url_base_name = 'api:mercado'
    model_name = Mercado

    def create_data(self):
        orcamento = mommy.make(Orcamento)
        return {'orcamento': orcamento.pk, 'valor': 100.0}

    def update_data(self):
        base = mommy.make(Orcamento)
        return {'valor': 200.0}


class SecaoListaViewSetTest(LoginRequiredMixin, ModelViewSetTestCase):
    url_base_name = 'api:secaolista'
    model_name = SecaoLista

    def create_data(self):
        return {'descricao': 'Test Section', 'ordem': 1}

    def update_data(self):
        return {'descricao': 'New Description'}


class ItensListaViewSetTest(LoginRequiredMixin, ModelViewSetTestCase):
    url_base_name = 'api:itenslista'
    model_name = ItensLista

    def create_data(self):
        secao = mommy.make(SecaoLista)
        return {'secao': secao.pk, 'descricao': 'Test Item', 'ordem': 1}

    def update_data(self):
        return {'descricao': 'New Item Description'}


class ItemCompraViewSetTest(LoginRequiredMixin, ModelViewSetTestCase):
    url_base_name = 'api:itemcompra'
    model_name = ItemCompra

    def create_data(self):
        secao = mommy.make(ListaCompras)
        item = mommy.make(ItensLista)
        return {'lista': secao.pk, 'item': item.pk, 'quantidade_sugerida': 1}

    def update_data(self):
        return {'comprado': True}


class ListaAtualViewTest(LoginRequiredMixin, TestCase):
    def test_verify_redirect(self):
        hoje = date.today()
        url = reverse('compras:lista-atual')
        redirect_url = reverse('compras:lista', kwargs={'ano': hoje.year, 'mes': hoje.month})
        mommy.make(ListaCompras, orcamento__ano=hoje.year, orcamento__mes=hoje.month)
        response = self.client.get(url)
        self.assertRedirects(response, redirect_url)


class ListaViewTest(LoginRequiredMixin, TestCase):
    def test_get(self):
        lista = mommy.make(ListaCompras)
        lista.orcamento.ano = abs(lista.orcamento.ano)
        lista.orcamento.mes = abs(lista.orcamento.mes)
        lista.orcamento.save()
        url = reverse('compras:lista', kwargs={'ano': lista.orcamento.ano, 'mes': lista.orcamento.mes})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['object'], lista)


class ItensListaTest(TestCase):
    def test_quantidade(self):
        item = mommy.make(ItensLista)
        quantidade_str = '%d %s' % (item.quantidade_sugerida, item.unidade)
        self.assertEquals(item.quantidade, quantidade_str)


class ItemCompraTest(TestCase):
    def test_quantidade(self):
        item = mommy.make(ItemCompra, _fill_optional=True)
        quantidade_str = '%d %s' % (item.quantidade_sugerida, item.unidade)
        self.assertEquals(item.quantidade, quantidade_str)

    def test_quantidade_do_item(self):
        item = mommy.make(ItemCompra)
        quantidade_str = '%d %s' % (item.item.quantidade_sugerida, item.item.unidade)
        self.assertEquals(item.quantidade, quantidade_str)


class ListaComprasViewTest(LoginRequiredMixin, TestCase):
    def test_get(self):
        qtd= randrange(13, 20)
        mommy.make(ListaCompras, _quantity=qtd)
        url = reverse('compras:listas')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['itens']), qtd)

    def test_get_empty(self):
        empty_message = 'Nenhuma lista cadastrada'.encode()
        url = reverse('compras:listas')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['itens']), 0)
        self.assertIn(empty_message, response.content)