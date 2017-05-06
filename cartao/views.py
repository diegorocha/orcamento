from django.views import generic

from cartao import models
from core.views import BaseViewMixin
from orcamento.models import Categoria, Orcamento


class CadastrarCompraCartaoView(BaseViewMixin, generic.TemplateView):
    template_name = 'cadastrar-compra-cartao.html'

    def get_context_data(self, **kwargs):
        context = super(CadastrarCompraCartaoView, self).get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['faturas'] = models.Fatura.objects.filter(aberta=True).order_by('orcamento', 'cartao')
        return context


class FecharFaturaView(BaseViewMixin, generic.TemplateView):
    template_name = 'fechar-fatura.html'

    def get_context_data(self, **kwargs):
        context = super(FecharFaturaView, self).get_context_data(**kwargs)
        context['faturas'] = models.Fatura.objects.filter(aberta=True).order_by('orcamento', 'cartao')
        context['orcamentos'] = Orcamento.objects.all()[:3]
        return context
