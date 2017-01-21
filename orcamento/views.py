import models
from datetime import date
from django.views import generic
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from core.views import BaseViewMixin


class OrcamentoAtual(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        hoje = date.today()
        return reverse('orcamento:orcamento', kwargs={'ano': hoje.year, 'mes': hoje.month})


class OrcamentoView(BaseViewMixin, generic.DetailView):
    template_name = 'orcamento.html'

    def get_object(self, queryset=None):
        return get_object_or_404(models.Orcamento, ano=self.kwargs['ano'], mes=self.kwargs['mes'])


class EstatisticaView(BaseViewMixin, generic.TemplateView):
    template_name = 'estatisticas.html'


class AjustarCategoriasView(BaseViewMixin, generic.TemplateView):
    template_name = 'ajustar-contas-sem-categoria.html'
