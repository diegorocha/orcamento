from django.views import generic

from cartao import models
from core.views import BaseViewMixin
from orcamento.models import Categoria


class CadastrarCompraCartaoView(BaseViewMixin, generic.TemplateView):
    template_name = 'cadastrar-compra-cartao.html'

    def get_context_data(self, **kwargs):
        context = super(CadastrarCompraCartaoView, self).get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['faturas'] = models.Fatura.objects.order_by('orcamento', 'cartao')
        return context
