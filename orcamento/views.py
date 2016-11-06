import models
from datetime import date
from django.views import generic
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


class OrcamentoAtual(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        hoje = date.today()
        return reverse('orcamento:orcamento', kwargs={'ano': hoje.year, 'mes': hoje.month})


class OrcamentoView(LoginRequiredMixin, generic.DetailView):
    template_name = 'orcamento.html'

    def get_object(self, queryset=None):
        return get_object_or_404(models.Orcamento, ano=self.kwargs['ano'], mes=self.kwargs['mes'])


class EstatisticaView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'estatisticas.html'


class AjustarCategoriasView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'ajustar-contas-sem-categoria.html'
