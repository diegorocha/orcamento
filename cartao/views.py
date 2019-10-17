from django.db.models.aggregates import Sum
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic.list import ListView
from simplejson import dumps

from cartao import models
from cartao.utils import estatistica_fatura
from core.views import BaseViewMixin
from orcamento.models import Categoria, Orcamento


class CadastrarCompraCartaoView(BaseViewMixin, generic.TemplateView):
    template_name = 'cadastrar-compra-cartao.html'
    permission_required = "cartao.add_compracartao"

    def get_context_data(self, **kwargs):
        context = super(CadastrarCompraCartaoView, self).get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['faturas'] = models.Fatura.objects.filter(aberta=True).order_by('orcamento', 'cartao')
        return context


class FecharFaturaView(BaseViewMixin, generic.TemplateView):
    template_name = 'fechar-fatura.html'
    permission_required = ('cartao.change_fatura', 'cartao.add_fatura')

    def get_context_data(self, **kwargs):
        context = super(FecharFaturaView, self).get_context_data(**kwargs)
        context['faturas'] = models.Fatura.objects.filter(aberta=True).order_by('orcamento', 'cartao')
        context['orcamentos'] = Orcamento.objects.all()[:3]
        return context


class FaturaView(BaseViewMixin, ListView):
    template_name = 'fatura.html'
    permission_required = 'cartao.change_fatura'

    def dispatch(self, request, *args, **kwargs):
        self.fatura = get_object_or_404(models.Fatura, id=self.kwargs['fatura_id'])
        return super(FaturaView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return models.CompraCartao.objects.filter(fatura=self.fatura)

    @property
    def total(self):
        return self.get_queryset().aggregate(valor_real=Sum('valor_real'), valor_dolar=Sum('valor_dolar'), valor_fatura=Sum('valor_fatura'))

    @property
    def parcelamento(self):
        queryset = self.get_queryset()
        data = {}
        data['a_vista'] = queryset.filter(parcelas=1).aggregate(valor_real=Sum('valor_real'))
        data['a_prazo'] = queryset.filter(parcelas__gte=2).aggregate(valor_real=Sum('valor_real'))
        return data

    @property
    def estatistica(self):
        estatistica = estatistica_fatura(self.fatura)
        return dumps(estatistica)


class ProximasFaturasView(BaseViewMixin, generic.TemplateView):
    template_name = 'proximas-faturas.html'

    def get_faturas(self):
        qtd = int(self.request.GET.get('qtd', 3))
        cartao = get_object_or_404(models.Cartao, id=self.kwargs['cartao_id'])
        fatura = cartao.faturas.filter(aberta=True).last()
        return fatura.get_proximas_faturas(qtd=qtd)


class SMSView(BaseViewMixin, generic.TemplateView):
    template_name = 'sms.html'
    permission_required = "cartao.add_compracartao"

    def get_context_data(self, **kwargs):
        context = super(SMSView, self).get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['faturas'] = models.Fatura.objects.filter(aberta=True).order_by('orcamento', 'cartao')
        return context


class CartaoRenataView(BaseViewMixin, generic.TemplateView):
    template_name = 'cartao-renata.html'

    def get_compras(self):
        return models.CompraCartao.objects.filter(
            categoria__descricao__iexact="Renata",
            fatura__aberta=True
        )

    def get_context_data(self, **kwargs):
        context = super(CartaoRenataView, self).get_context_data(**kwargs)
        compras = self.get_compras()
        context['categorias'] = models.Categoria.objects.all()
        context['compras'] = compras
        context['totais'] = compras.aggregate(
            real=Sum('valor_real'),
            dolar=Sum('valor_dolar'),
        )
        context["pode_editar_categoria"] = self.request.user.has_perm("cartao.change_compracartao")
        return context
