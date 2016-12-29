from datetime import date
from model_mommy import mommy
from django.test import TestCase
from orcamento.models import Orcamento
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from compras.models import Mercado, SecaoLista, ItensLista, ListaCompras, ItemCompra


class LoginRequiredMixin(TestCase):
    def setUp(self):
        super(LoginRequiredMixin, self).setUp()
        username = 'admin'
        password = '4dm1n'
        User.objects.create_user(username=username, password=password, is_staff=True)
        self.client.login(username=username, password=password)


class ModelViewSetTestCase(APITestCase):
    url_base_name = None
    model_name = None

    def setUp(self):
        self.endpoint = reverse('%s-list' % self.url_base_name) if self.url_base_name else None

    def get_detail_endpoint(self, pk):
        return reverse('%s-detail' % self.url_base_name, args=(pk,)) if self.url_base_name else None

    def create_data(self):
        return {}

    def update_data(self):
        return {}

    def test_list(self):
        if self.model_name:
            mommy.make(self.model_name, _fill_optional=True, _quantity=20)
            count = self.model_name.objects.count()
            response = self.client.get(self.endpoint)
            self.assertEquals(response.status_code, 200)
            data = response.json()
            print data
            self.assertEquals(len(data), count)

    def test_create(self):
        if self.model_name:
            response = self.client.post(self.endpoint, self.create_data(), format='json')
            self.assertEquals(response.status_code, 201)
            data = response.json()
            pk = data["id"]
            instance = self.model_name.objects.filter(pk=pk).first()
            self.assertIsNotNone(instance)

    def test_retrieve(self):
        if self.model_name:
            instance = mommy.make(self.model_name, _fill_optional=True)
            response = self.client.get(self.get_detail_endpoint(instance.pk))
            self.assertEquals(response.status_code, 200)
            data = response.json()
            self.assertIsNotNone(data)

    def test_update(self):
        if self.model_name:
            instance = mommy.make(self.model_name, _fill_optional=True)
            detail_endpoint = self.get_detail_endpoint(instance.pk)
            response = self.client.get(detail_endpoint)
            self.assertEquals(response.status_code, 200)
            data = response.json()
            new_data = self.update_data()
            data.update(new_data)
            response = self.client.put(detail_endpoint, data, format='json')
            self.assertEquals(response.status_code, 200)
            updated_instance = self.model_name.objects.get(pk=instance.pk)
            for key, value in new_data.items():
                self.assertEquals(getattr(updated_instance, key), value)

    def test_partial_update(self):
        if self.model_name:
            instance = mommy.make(self.model_name, _fill_optional=True)
            detail_endpoint = self.get_detail_endpoint(instance.pk)
            new_data = self.update_data()
            response = self.client.patch(detail_endpoint, new_data, format='json')
            self.assertEquals(response.status_code, 200)
            updated_instance = self.model_name.objects.get(pk=instance.pk)
            for key, value in new_data.items():
                self.assertEquals(getattr(updated_instance, key), value)

    def test_delete(self):
        if self.model_name:
            instance = mommy.make(self.model_name, _fill_optional=True)
            detail_endpoint = self.get_detail_endpoint(instance.pk)
            response = self.client.delete(detail_endpoint)
            self.assertEquals(response.status_code, 204)
            deleted_instance = self.model_name.objects.filter(pk=instance.pk).first()
            self.assertIsNone(deleted_instance)


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
